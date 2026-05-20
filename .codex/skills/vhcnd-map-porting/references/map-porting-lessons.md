# Map Porting Lessons

## Ba Lang Huyen Fixes To Preserve

Use this reference when porting or fixing map visuals in the H5 runtime.

### Evidence From PC Source

- `SceneDataDef.h`: `REGION_GROUND_LAYER_FILE_INDEX = 4`, `REGION_BUILDIN_OBJ_FILE_INDEX = 5`.
- `SceneDataDef.h`: `KBuildinObj` stores `ImgPos1..4`, `nImgWidth`, `nImgHeight`, image path, animation fields, `oPos1`, and `oPos2`.
- `KIpotLeaf::PaintABuildinObject`: static build-ins set `RUIMAGE_RENDER_FLAG_FRAME_DRAW` and use `ImgPos1/ImgPos3`; non-point objects draw as `RU_T_IMAGE_4` with all four `ImgPos` corners.
- `KIpotBranch::PaintABranchObject`: branch/quad build-ins can be partial multi-piece images; independent scaling creates visible gaps.
- `KRepresentShell2/3::CoordinateTransform`: `nX = nX - m_nLeft`; `nY = nY / 2 - m_nTop - ((nZ * 887) >> 10)`.

### Failure: Vertical Stretch

Bad behavior:

- Bake map canvas at `sourceWorldHeight / 2`.
- Resize the final image back to full `sourceWorldHeight`.
- Set runtime `worldSize.height` to full source height.

Result:

- Gates, roofs, buildings, and roads look too tall.
- Map feels like it was distorted by portrait mode, but the actual cause is post-bake vertical stretching.

Correct behavior:

- Bake and save background at render height, not source height.
- Store `sourceWorldSize` for provenance.
- Store runtime `worldSize` as render size.
- For Ba Lang Huyen, source is `16896 x 20480`, render/runtime is `16896 x 10240`.
- Tile count becomes `45` for `2048` tiles instead of `90`.

### Failure: Scaling Quad Pieces

Bad behavior:

- Apply the same visual scale to all build-ins.
- Scale `LINE`/`TREE`/quad build-ins independently.

Result:

- Multi-part houses, roofs, walls, and gates show holes or seams.

Correct behavior:

- Keep quad build-ins at `1.0` unless implementing group-scale over the full object cluster.
- Only scale point/standalone build-ins for H5 readability.
- Ba Lang Huyen current policy: `POINT = 0.275`, `QUAD = 1.0`.

### Required Smoke Assertions

Smoke tests should lock:

- Map identity and `.wor`/minimap file ids.
- `sourceWorldSize` vs runtime `worldSize`.
- Cache version after regeneration.
- Tile count and file existence.
- `coordinateMode` containing `no post-bake vertical stretch` and `z*887>>10`.
- `buildinPointVisualScale` and `buildinQuadVisualScale`.
- Enemy list excludes immobile NPCs such as `Bao cat`, `Moc nhan`, `Coc go`.
