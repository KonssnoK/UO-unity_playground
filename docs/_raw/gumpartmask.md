# gumpartmask

Auto-generated from `tools/ghidra/ghidra_dump.json`.

Functions discovered via xrefs from strings matching: `GumpArtMask, gumpartmask, GumpArtMaskData`

Total: 5 unique decompiled functions.

---

## `FUN_0058e1a0` @ 0058e1a0

- **signature**: `undefined FUN_0058e1a0(void)`
- **triggered by strings**:
  - `s_TileArtLegacy\_00cb8a08`
  - `s_TileArtEnhanced\_00cb8a18`
  - `s_GumpArtMask\_00cb8a2c`

```c

void __fastcall FUN_0058e1a0(char *param_1)

{
  int *piVar1;
  char *pcVar2;
  char *pcVar3;
  uint uVar4;
  undefined4 *unaff_ESI;
  
  piVar1 = unaff_ESI + 1;
  *unaff_ESI = SimpleTextureFileLocation::vftable;
  *piVar1 = 0;
  unaff_ESI[2] = 0;
  unaff_ESI[3] = 0;
  pcVar2 = param_1;
  do {
    pcVar3 = pcVar2;
    pcVar2 = pcVar3 + 1;
  } while (*pcVar3 != '\0');
  FUN_0058ecd0(param_1,pcVar3);
  unaff_ESI[5] = 1;
  *unaff_ESI = SpriteTextureFileLocation::vftable;
  uVar4 = FUN_0058eab0("Textures\\");
  if (uVar4 < (unaff_ESI[2] - *piVar1) - 1U) {
    unaff_ESI[5] = 8;
    return;
  }
  uVar4 = FUN_0058eab0("TileArtLegacy\\");
  if (uVar4 < (unaff_ESI[2] - *piVar1) - 1U) {
    unaff_ESI[5] = 0x16;
    return;
  }
  uVar4 = FUN_0058eab0("TileArtEnhanced\\");
  if (uVar4 < (unaff_ESI[2] - *piVar1) - 1U) {
    unaff_ESI[5] = 0x1a;
    return;
  }
  uVar4 = FUN_0058eab0("GumpArtMask\\");
  if (uVar4 < (unaff_ESI[2] - *piVar1) - 1U) {
    unaff_ESI[5] = 0x1b;
  }
  return;
}

```

---

## `FUN_0058e280` @ 0058e280

- **signature**: `undefined FUN_0058e280(void)`
- **triggered by strings**:
  - `s_TileArtLegacy\_00cb8a08`
  - `s_TileArtEnhanced\_00cb8a18`
  - `s_GumpArtMask\_00cb8a2c`

```c

undefined4 * __fastcall FUN_0058e280(undefined4 *param_1)

{
  int *piVar1;
  uint uVar2;
  
  FUN_0058e0b0();
  piVar1 = param_1 + 1;
  *param_1 = SpriteTextureFileLocation::vftable;
  uVar2 = FUN_0058eab0("Textures\\");
  if (uVar2 < (param_1[2] - *piVar1) - 1U) {
    param_1[5] = 8;
    return param_1;
  }
  uVar2 = FUN_0058eab0("TileArtLegacy\\");
  if (uVar2 < (param_1[2] - *piVar1) - 1U) {
    param_1[5] = 0x16;
    return param_1;
  }
  uVar2 = FUN_0058eab0("TileArtEnhanced\\");
  if (uVar2 < (param_1[2] - *piVar1) - 1U) {
    param_1[5] = 0x1a;
    return param_1;
  }
  uVar2 = FUN_0058eab0("GumpArtMask\\");
  if (uVar2 < (param_1[2] - *piVar1) - 1U) {
    param_1[5] = 0x1b;
  }
  return param_1;
}

```

---

## `FUN_0058e330` @ 0058e330

- **signature**: `undefined FUN_0058e330(void)`
- **triggered by strings**:
  - `s_WorldArt_00cb8a3c`
  - `s_WorldArt\ref_00cb8a48`
  - `s_TileArtLegacy_00cb8a58`
  - `s_TileArtEnhanced_00cb8a68`
  - `s_GumpArtMask_00cb8a78`

```c

bool __fastcall FUN_0058e330(int param_1)

{
  int *piVar1;
  uint uVar2;
  
  if (*(int *)(DAT_00e3d520 + 0x160 + *(int *)(param_1 + 0x14) * 4) != 1) {
    return true;
  }
  piVar1 = (int *)(param_1 + 4);
  uVar2 = FUN_0058eab0("WorldArt");
  if (uVar2 < (*(int *)(param_1 + 8) - *piVar1) - 1U) {
    uVar2 = FUN_0058eab0("WorldArt\\ref");
    return uVar2 < (*(int *)(param_1 + 8) - *piVar1) - 1U;
  }
  uVar2 = FUN_0058eab0("Textures\\");
  if ((*(int *)(param_1 + 8) - *piVar1) - 1U <= uVar2) {
    uVar2 = FUN_0058eab0("TileArtLegacy");
    if ((*(int *)(param_1 + 8) - *piVar1) - 1U <= uVar2) {
      uVar2 = FUN_0058eab0("TileArtEnhanced");
      if ((*(int *)(param_1 + 8) - *piVar1) - 1U <= uVar2) {
        uVar2 = FUN_0058eab0("GumpArtMask");
        return (*(int *)(param_1 + 8) - *piVar1) - 1U <= uVar2;
      }
    }
  }
  return false;
}

```

---

## `FUN_005960f0` @ 005960f0

- **signature**: `undefined FUN_005960f0(void)`
- **triggered by strings**:
  - `s_Build\GumpArtMask\0%d.dds_00cb915c`

```c

undefined4 __thiscall FUN_005960f0(int param_1)

{
  int iVar1;
  int iVar2;
  uint uVar3;
  float *pfVar4;
  byte bVar5;
  float fVar6;
  char cVar7;
  float fVar8;
  int *piVar9;
  undefined **ppuVar10;
  uint uVar11;
  LONG LVar12;
  undefined4 uVar13;
  undefined2 in_FPUControlWord;
  int in_stack_00000010;
  float local_454;
  int local_450;
  float local_44c;
  float local_448;
  int aiStack_444 [3];
  longlong lStack_438;
  int *apiStack_430 [2];
  undefined1 auStack_428 [24];
  undefined1 auStack_410 [8];
  undefined1 auStack_408 [1028];
  
  *(undefined4 *)(param_1 + 0x3c) = 1;
  iVar1 = *(int *)(*(int *)(in_stack_00000010 + 0x28) + 0x30);
  iVar2 = **(int **)(*(int *)(in_stack_00000010 + 0x28) + 0x20);
  if ((iVar1 == 0) || (*(short *)(iVar1 + 10) == 0)) {
    aiStack_444[2] = 0;
  }
  else {
    aiStack_444[2] = **(int **)(iVar1 + 4);
  }
  if (iVar2 != 0) {
    piVar9 = *(int **)(param_1 + 0x120);
    *(undefined1 *)(piVar9 + 3) = 0;
    piVar9[1] = *(ushort *)(iVar2 + 4) >> 0xc & 3;
    piVar9[2] = *(byte *)(iVar2 + 5) & 0xf;
    if (*piVar9 != *(int *)(iVar2 + 8)) {
      *piVar9 = *(int *)(iVar2 + 8);
    }
    if ((*(int *)(iVar2 + 0xc) != 0) && (*(char *)(*(int *)(iVar2 + 0xc) + 0x1c) != '\0')) {
      FUN_00696d30();
    }
    FUN_009b1750();
  }
  local_448 = 0.0;
  local_44c = 0.0;
  local_450 = 1;
  fVar8 = (float)FUN_00678b10("CustomShaderData");
  local_454 = fVar8;
  piVar9 = (int *)FUN_0067c960();
  uVar11 = 0;
  if (piVar9 != (int *)0x0) {
    for (ppuVar10 = (undefined **)(**(code **)(*piVar9 + 8))(); ppuVar10 != (undefined **)0x0;
        ppuVar10 = (undefined **)ppuVar10[1]) {
      if (ppuVar10 == &PTR_s_NiFloatsExtraData_00de4334) {
        bVar5 = 1;
        goto LAB_005961e4;
      }
    }
    bVar5 = 0;
LAB_005961e4:
    uVar11 = -(uint)bVar5 & (uint)piVar9;
  }
  if ((fVar8 != 0.0) && (LVar12 = InterlockedDecrement((LONG *)((int)local_454 + -8)), LVar12 == 1))
  {
    FUN_00678e00(&local_454);
  }
  fVar8 = local_448;
  if (uVar11 != 0) {
    uVar3 = *(uint *)(uVar11 + 0xc);
    if (uVar3 == 0) {
      fVar8 = 0.0;
    }
    else {
      fVar8 = **(float **)(uVar11 + 0x10);
    }
    if (uVar3 < 2) {
      local_44c = 0.0;
    }
    else {
      local_44c = *(float *)(*(int *)(uVar11 + 0x10) + 4);
    }
    lStack_438._0_4_ = (int *)(longlong)ROUND(local_44c);
    local_44c = (float)(int *)lStack_438;
    if (uVar3 < 3) {
      local_454 = 0.0;
    }
    else {
      local_454 = *(float *)(*(int *)(uVar11 + 0x10) + 8);
    }
    fVar6 = local_454;
    local_454 = (float)CONCAT22(local_454._2_2_,in_FPUControlWord);
    lStack_438 = (longlong)ROUND(fVar6);
    local_450 = (int)(int *)lStack_438;
  }
  pfVar4 = *(float **)(param_1 + 0x230);
  *pfVar4 = fVar8;
  pfVar4[1] = fVar8;
  pfVar4[2] = fVar8;
  pfVar4[3] = fVar8;
  if ((fVar8 != 0.0) && (*(int *)(param_1 + 0x26c) == 0)) {
    aiStack_444[0] = 0;
    aiStack_444[1] = 0;
    FUN_0058e1a0();
    (**(code **)(**(int **)(DAT_00e3d524 + 0xa8) + 4))(&local_454,auStack_428,aiStack_444,0,4);
    if ((local_454._0_1_ != '\0') && (aiStack_444[0] != 0)) {
      local_448 = *(float *)(aiStack_444[0] + 4);
      if (local_448 != 0.0) {
        InterlockedIncrement((LONG *)((int)local_448 + 4));
      }
      FUN_0042b060(&local_448);
      FUN_00420090();
    }
    FUN_0041c460();
    FUN_0041c420();
  }
  iVar1 = *(int *)(param_1 + 0x26c);
  if (iVar1 == 0) {
    **(undefined4 **)(param_1 + 0x180) = 0;
  }
  else {
    piVar9 = *(int **)(param_1 + 0x140);
    *(undefined1 *)(piVar9 + 3) = 0;
    piVar9[1] = 0;
    piVar9[2] = 0;
    if (*piVar9 != iVar1) {
      *piVar9 = iVar1;
    }
    **(undefined4 **)(param_1 + 0x180) = 1;
  }
  if (aiStack_444[2] == 0) {
    **(undefined4 **)(param_1 + 0x1a0) = 0;
    if ((local_44c == 0.0) || (local_450 == 0)) goto LAB_0059666b;
    if (local_44c != *(float *)(param_1 + 0x274)) {
      aiStack_444[0] = 0;
      aiStack_444[1] = 0;
      if (local_450 == 1) {
        FUN_005bfd30(local_44c);
        if ((apiStack_430[0] != (int *)0x0) &&
           (cVar7 = (**(code **)(*apiStack_430[0] + 0x54))(0x40000,0), cVar7 != '\0')) {
          FUN_004376a0();
          fVar8 = (float)FUN_00457b20(0);
          local_448 = fVar8;
          FUN_00460480();
          piVar9 = (int *)lStack_438;
          if (((int *)lStack_438 != (int *)0x0) &&
             (uVar11 = (**(code **)(*(int *)lStack_438 + 4))(), 2 < uVar11)) {
            (**(code **)(*piVar9 + 8))(auStack_410,2);
            FUN_0058e1a0();
            FUN_0042e230();
            (**(code **)(**(int **)(DAT_00e3d524 + 0xa8) + 4))
                      (&stack0xfffffba4,apiStack_430,&local_44c,0,4);
            if ((local_454._0_1_ != '\0') && (aiStack_444[0] != 0)) {
              uVar13 = FUN_0041a210();
              FUN_0042b060(uVar13);
              FUN_00420090();
              iVar1 = *(int *)(param_1 + 0x270);
              piVar9 = *(int **)(param_1 + 0x160);
              *(undefined1 *)(piVar9 + 3) = 0;
              piVar9[1] = 0;
              piVar9[2] = 0;
              if (*piVar9 != iVar1) {
                *piVar9 = iVar1;
              }
              **(undefined4 **)(param_1 + 0x1a0) = 1;
              *(float *)(param_1 + 0x274) = local_44c;
              fVar8 = local_448;
            }
            FUN_0041c460();
          }
          if (fVar8 != 0.0) {
            FUN_0042ca80();
          }
          FUN_00449300();
        }
        FUN_0040ca90();
      }
      else if (local_450 == 2) {
        FUN_009a3ada(auStack_408,0x400,"Build\\GumpArtMask\\0%d.dds",(int)local_44c + 1000000);
        FUN_0058e1a0();
        (**(code **)(**(int **)(DAT_00e3d524 + 0xa8) + 4))(&local_454,auStack_428,aiStack_444,0,4);
        if ((local_454._0_1_ != '\0') && (aiStack_444[0] != 0)) {
          uVar13 = FUN_0041a210();
          FUN_0042b060(uVar13);
          FUN_00420090();
          iVar1 = *(int *)(param_1 + 0x270);
          piVar9 = *(int **)(param_1 + 0x160);
          *(undefined1 *)(piVar9 + 3) = 0;
          piVar9[1] = 0;
          piVar9[2] = 0;
          if (*piVar9 != iVar1) {
            *piVar9 = iVar1;
          }
          **(undefined4 **)(param_1 + 0x1a0) = 1;
          *(float *)(param_1 + 0x274) = local_44c;
        }
        FUN_0041c460();
        FUN_0041c420();
        goto LAB_0059666b;
      }
      FUN_0041c420();
      goto LAB_0059666b;
    }
    if (*(int *)(param_1 + 0x270) == 0) goto LAB_0059666b;
  }
  else {
    piVar9 = *(int **)(param_1 + 0x160);
    *(undefined1 *)(piVar9 + 3) = 0;
    piVar9[1] = *(ushort *)(aiStack_444[2] + 4) >> 0xc & 3;
    piVar9[2] = *(byte *)(aiStack_444[2] + 5) & 0xf;
    if (*piVar9 != *(int *)(aiStack_444[2] + 8)) {
      *piVar9 = *(int *)(aiStack_444[2] + 8);
    }
  }
  **(undefined4 **)(param_1 + 0x1a0) = 1;
LAB_0059666b:
  iVar1 = *(int *)(param_1 + 0x1c);
  if (*(int *)(iVar1 + 0x730) != 0) {
    (**(code **)(**(int **)(iVar1 + 0x2238) + 0xe4))(*(int **)(iVar1 + 0x2238),0xc2,0);
    *(undefined4 *)(iVar1 + 0x730) = 0;
  }
  return 0;
}

```

---

## `FUN_00a70e5a` @ 00a70e5a

- **signature**: `undefined FUN_00a70e5a(void)`
- **triggered by strings**:
  - `s_tileart.uop_00d02c50`
  - `s_TerrainDefinition.uop_00d02c8c`
  - `s_Texture.uop_00d02cdc`
  - `s_EffectTexture.uop_00d02cf4`
  - `s_TerrainChunk.uop_00d02d20`
  - `s_RadarMapTexture.uop_00d02d34`
  - `s_LegacyTerrain.uop_00d02d78`
  - `s_TerrainTexture.uop_00d02d8c`
  - `s_LegacyTexture.uop_00d02e00`
  - `s_EnhancedTexture.uop_00d02e20`
  - `s_GumpArtMask.uop_00d02e34`

```c

undefined4 FUN_00a70e5a(void)

{
  undefined4 uVar1;
  int unaff_EBP;
  undefined1 auStack_44 [20];
  undefined4 uStack_30;
  int iStack_2c;
  
  FUN_00b7b70c();
  uVar1 = *(undefined4 *)(unaff_EBP + 8);
  iStack_2c = 0;
  uStack_30 = 0xa70e76;
  FUN_00a70e45();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet0.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 1;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa70eb9;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa70ec5;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet1.uop");
  *(undefined4 *)(unaff_EBP + -4) = 2;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 3;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa70f05;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa70f11;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet2.uop");
  *(undefined4 *)(unaff_EBP + -4) = 4;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 5;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa70f51;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa70f5d;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet3.uop");
  *(undefined4 *)(unaff_EBP + -4) = 6;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 7;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa70f9d;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa70fa9;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet4.uop");
  *(undefined4 *)(unaff_EBP + -4) = 8;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 9;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa70fe9;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa70ff5;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet5.uop");
  *(undefined4 *)(unaff_EBP + -4) = 10;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0xb;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71035;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71041;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facet6.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0xc;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0xd;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71081;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa7108d;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("tileart.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0xe;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0xf;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa710cd;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa710d9;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("string_dictionary.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x10;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x11;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71115;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71121;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("AnimationDefinition.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x12;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x13;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71161;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa7116d;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("TerrainDefinition.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x14;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x15;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa711ad;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa711b9;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("EffectDefinitionCollection.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x16;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x17;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa711f9;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71205;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("AnimationSequence.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x18;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x19;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71245;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71251;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Texture.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x1a;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x1b;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71291;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa7129d;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Audio.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x1c;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x1d;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa712dd;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa712e9;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("EffectTexture.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x1e;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x1f;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71329;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71335;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("LocalizedStrings.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x20;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x21;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71375;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71381;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("TerrainChunk.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x22;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x23;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa713c1;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa713cd;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("RadarMapTexture.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x24;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x25;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa7140d;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71419;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Interface.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x26;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x27;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71459;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71465;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("GameData.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x28;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x29;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa714a5;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa714b1;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("MainMisc.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x2a;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x2b;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa714f1;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa714fd;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("LegacyTerrain.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x2c;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x2d;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa7153d;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71549;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("TerrainTexture.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x2e;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x2f;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71589;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71595;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("SystemTextures.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x30;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x31;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa715d5;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa715e1;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Paperdoll.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x32;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x33;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71621;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa7162d;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Hues.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x34;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x35;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa7166d;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71679;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("MultiCollection.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x36;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x37;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa716b9;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa716c5;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Shaders.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x38;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x39;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71705;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71711;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("Waypoint.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x3a;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x3b;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71751;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa7175d;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("LegacyTexture.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x3c;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x3d;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa7179d;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa717a9;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("facets.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x3e;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x3f;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa717e9;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa717f5;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("EnhancedTexture.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x40;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x41;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71835;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa71841;
  FUN_00403770();
  *(undefined1 **)(unaff_EBP + 8) = auStack_44;
  FUN_00403700("GumpArtMask.uop");
  *(undefined4 *)(unaff_EBP + -4) = 0x42;
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = FUN_00a70df8(uVar1,unaff_EBP + -0x28);
  *(undefined4 *)(unaff_EBP + -4) = 0x43;
  if (*(uint *)(iStack_2c + 0x18) < 0x10) {
    iStack_2c = iStack_2c + 4;
  }
  else {
    iStack_2c = *(int *)(iStack_2c + 4);
  }
  uStack_30 = 0xa71881;
  FUN_0098e793();
  *(undefined4 *)(unaff_EBP + -4) = 0xffffffff;
  iStack_2c = 0xa7188d;
  FUN_00403770();
  iStack_2c = 0xa71892;
  FUN_00a71a4d();
  iStack_2c = 0xa71897;
  FUN_00a71b2d();
  ExceptionList = *(void **)(unaff_EBP + -0xc);
  return 0;
}

```

---

