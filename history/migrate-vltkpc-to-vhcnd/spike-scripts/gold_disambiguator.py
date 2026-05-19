import json
import csv
import sys
import os

def load_vhcnd_gold(path):
    items = []
    with open(path, 'r', encoding='cp1258', errors='replace') as f:
        # Skip header, read raw lines
        lines = f.readlines()
        header = lines[0].strip().split('\t')
        for i, line in enumerate(lines[1:]):
            cols = line.strip().split('\t')
            row = dict(zip(header, cols))

            items.append({
                'line': i + 2,
                'name': row.get('Ä‚Ă»Â³Ă†'),
                'genre': row.get('ItemGenre'),
                'detail': row.get('DetailType'),
                'particular': row.get('ParticularType'),
                'sprite': row.get('Â¶Â¯Â»Â\xadĂĂ„Â¼â‚«Ä‚Ă»', '').lower().replace('/', '\\').strip(),
                'series': row.get('nSeries'),
                'level': row.get('nLevel'),
                'm1': row.get('Magic1'), 'min1': row.get('Min1'), 'max1': row.get('Max1'),
                'm2': row.get('Magic2'), 'min2': row.get('Min2'), 'max2': row.get('Max2'),
                'm3': row.get('Magic3'), 'min3': row.get('Min3'), 'max3': row.get('Max3'),
                'm4': row.get('Magic4'), 'min4': row.get('Min4'), 'max4': row.get('Max4'),
                'm5': row.get('Magic5'), 'min5': row.get('Min5'), 'max5': row.get('Max5'),
                'm6': row.get('Magic6'), 'min6': row.get('Min6'), 'max6': row.get('Max6'),
                'm7': row.get('Magic7'), 'min7': row.get('Min7'), 'max7': row.get('Max7'),
                'r1': row.get('Require1'), 'd1': row.get('Data1'),
                'r2': row.get('Require2'), 'd2': row.get('Data2'),
                'r3': row.get('Require3'), 'd3': row.get('Data3'),
                'r4': row.get('Require4'), 'd4': row.get('Data4'),
                'r5': row.get('Require5'), 'd5': row.get('Data5'),
                'r6': row.get('Require6'), 'd6': row.get('Data6'),
                'setId': row.get('SetID') or row.get('SetId'),
                'defm1': row.get('DefMagic1') # This might be the source line reference in VHCND!
            })
    return items

def main():
    h5_path = '/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-index.json'
    vhcnd_path = '/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt'

    with open(h5_path, 'r') as f:
        h5_data = json.load(f)

    h5_gold = [v for v in h5_data['items'] if v.get('source', {}).get('path', '').endswith('GoldItem.txt')]
    vhcnd_gold = load_vhcnd_gold(vhcnd_path)

    mapping = []
    unresolved = []

    for h5_item in h5_gold:
        matches = []
        h5_fields = h5_item['itemFields']
        h5_sprite = h5_fields['inventorySprite'].lower().strip()
        if not h5_sprite.startswith('\\'):
             h5_sprite = '\\' + h5_sprite

        potential_matches = []
        for v_item in vhcnd_gold:
            v_sprite = v_item['sprite']
            if not v_sprite.startswith('\\'):
                v_sprite = '\\' + v_sprite

            # Identity match (excluding sprite)
            if (str(h5_fields['genre']) == str(v_item['genre']) and
                str(h5_fields['detailType']) == str(v_item['detail']) and
                str(h5_fields['particularType']) == str(v_item['particular'])):

                score = 0

                # Check sprite similarity
                if h5_sprite == v_sprite:
                    score += 100
                elif h5_sprite[:-5] == v_sprite[:-5]:
                    score += 80
                elif h5_sprite.split('\\')[-1] == v_sprite.split('\\')[-1]: # Same file name
                    score += 70

                # DefMagic1 - check if it matches H5 source line
                if str(v_item.get('defm1')) == str(h5_item['source']['line'] - 1): # VHCND often uses 0-based or offset line
                    score += 50

                # Series
                if str(h5_fields.get('series')) == str(v_item['series']):
                    score += 30

                # Level
                if str(h5_fields.get('level')) == str(v_item['level']):
                    score += 10

                # Requirements match
                h5_reqs = {int(r['type']): int(r['value']) for r in h5_item.get('requirements', [])}
                v_reqs = {}
                for i in range(1, 7):
                    rt = v_item.get(f'r{i}')
                    rd = v_item.get(f'd{i}')
                    if rt and rd and rt != '' and rt != '0':
                        v_reqs[int(rt)] = int(rd)

                req_match_count = 0
                for rt, rv in h5_reqs.items():
                    if v_reqs.get(rt) == rv:
                        req_match_count += 1

                if len(h5_reqs) > 0:
                    score += (req_match_count / len(h5_reqs)) * 20
                elif len(v_reqs) == 0:
                    score += 20

                # Magic attributes match
                h5_magics = {int(m['type']): (int(m['ranges'][0]['min']), int(m['ranges'][0]['max'])) for m in h5_item.get('magicAttributes', [])}
                v_magics = {}
                for i in range(1, 8):
                    mt = v_item.get(f'm{i}')
                    mi = v_item.get(f'min{i}')
                    ma = v_item.get(f'max{i}')
                    if mt and mi and ma and mt != '' and mt != '0':
                        v_magics[int(mt)] = (int(mi), int(ma))

                magic_match_count = 0
                for mt, mrange in h5_magics.items():
                    vrange = v_magics.get(mt)
                    if vrange and vrange == mrange:
                        magic_match_count += 1

                if len(h5_magics) > 0:
                    score += (magic_match_count / len(h5_magics)) * 40
                elif len(v_magics) == 0:
                    score += 40

                if score > 0:
                    potential_matches.append({'item': v_item, 'score': score})

        if potential_matches:
            potential_matches.sort(key=lambda x: x['score'], reverse=True)
            best_score = potential_matches[0]['score']
            tied = [m for m in potential_matches if m['score'] == best_score]

            if len(tied) == 1:
                mapping.append({
                    'h5_id': h5_item['originalName'],
                    'vhcnd_line': tied[0]['item']['line'],
                    'confidence': 'high' if best_score >= 120 else 'medium',
                    'reason': f'Score {best_score:.2f}',
                    'h5_sprite': h5_sprite,
                    'v_sprite': tied[0]['item']['sprite']
                })
            else:
                unresolved.append({'h5_id': h5_item['originalName'], 'matches': [m['item']['line'] for m in tied], 'reason': 'Score tie', 'max_score': best_score})
        else:
            unresolved.append({'h5_id': h5_item['originalName'], 'matches': [], 'reason': 'No match found'})

    print(f"Total H5 Gold Items: {len(h5_gold)}")
    print(f"Resolved: {len(mapping)}")
    print(f"Unresolved: {len(unresolved)}")

    with open('history/migrate-vltkpc-to-vhcnd/spike-scripts/gold_mapping.json', 'w') as f:
        json.dump({'mapping': mapping, 'unresolved': unresolved}, f, indent=2)

if __name__ == '__main__':
    main()
