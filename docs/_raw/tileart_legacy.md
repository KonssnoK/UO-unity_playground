# tileart_legacy

Auto-generated from `tools/ghidra/ghidra_dump.json`.

Functions discovered via xrefs from strings matching: `TileArtLegacy, %08d_LegacyTileArt, tileartlegacy, LegacyTileArt`

Total: 5 unique decompiled functions.

---

## `FUN_0051af20` @ 0051af20

- **signature**: `undefined FUN_0051af20(void)`
- **triggered by strings**:
  - `s_%08d_LegacyTileArt_00cae7f4`

```c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4
FUN_0051af20(uint param_1,undefined4 *param_2,undefined4 *param_3,float *param_4,uint *param_5,
            uint *param_6,float *param_7,int *param_8,int *param_9)

{
  float fVar1;
  int iVar2;
  undefined4 *puVar3;
  float fVar4;
  char cVar5;
  int *piVar6;
  undefined4 unaff_EBX;
  uint uVar7;
  uint uVar8;
  ushort in_FPUControlWord;
  float10 fVar9;
  int *piVar10;
  float fVar11;
  uint unaff_retaddr;
  float fVar12;
  undefined6 uStack_bc;
  int *local_b8;
  int *local_b4;
  undefined4 *local_b0 [2];
  longlong local_a8;
  int iStack_a0;
  undefined4 uStack_9c;
  int iStack_98;
  undefined8 uStack_94;
  float fStack_88;
  undefined4 uStack_84;
  undefined4 uStack_80;
  uint uStack_7c;
  uint uStack_78;
  undefined1 uStack_70;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  float fStack_4c;
  uint uStack_48;
  int iStack_44;
  int iStack_40;
  undefined1 auStack_3c [36];
  undefined1 auStack_18 [16];
  undefined4 uStack_8;
  uint uStack_4;
  
  _uStack_bc = CONCAT44(local_b8,unaff_EBX);
  local_b4 = (int *)(param_1 & 0xffff);
  FUN_0051e6c0(&local_b4);
  if (local_b8 != DAT_00e3a068) {
    local_b8[0xf] = local_b8[0xf] + 1;
    fVar1 = DAT_00c9d1a0;
    *param_5 = local_b8[4];
    *param_6 = local_b8[5];
    iVar2 = local_b8[6];
    *param_9 = local_b8[7];
    *param_8 = iVar2;
    *param_7 = fVar1;
    FUN_004043d0(local_b8 + 8,0,0xffffffff);
    if (((param_2 != (undefined4 *)0x0) && (param_3 != (undefined4 *)0x0)) &&
       ((puVar3 = (undefined4 *)*param_8, param_2 < puVar3 || (param_3 < (undefined4 *)*param_9))))
    {
      fVar1 = (float)(int)puVar3;
      if ((int)puVar3 < 0) {
        fVar1 = fVar1 + _DAT_00d0a0dc;
      }
      fVar4 = (float)(int)param_2;
      if ((int)param_2 < 0) {
        fVar4 = fVar4 + _DAT_00d0a0dc;
      }
      local_b4 = (int *)(fVar4 / fVar1);
      local_b0[0] = param_3;
      fVar4 = (float)(int)param_3;
      if ((int)param_3 < 0) {
        fVar4 = fVar4 + _DAT_00d0a0dc;
      }
      fVar11 = (float)*param_9;
      if (*param_9 < 0) {
        fVar11 = fVar11 + _DAT_00d0a0dc;
      }
      piVar10 = (int *)(fVar4 / fVar11);
      _uStack_bc = CONCAT44(piVar10,fVar12);
      if ((float)local_b4 < (float)piVar10) {
        piVar10 = local_b4;
      }
      *param_7 = (float)piVar10;
      fVar9 = (float10)FUN_00457180(fVar1 * *param_7);
      iVar2 = *param_9;
      uStack_bc = CONCAT24(in_FPUControlWord,fVar12);
      local_b4 = (int *)(in_FPUControlWord | 0xc00);
      local_a8 = (longlong)ROUND(fVar9);
      *param_8 = (int)(int *)local_a8;
      fVar1 = (float)*param_9;
      if (iVar2 < 0) {
        fVar1 = fVar1 + _DAT_00d0a0dc;
      }
      fVar9 = (float10)FUN_00457180(fVar1 * *param_7);
      local_a8._0_4_ = (int *)(longlong)ROUND(fVar9);
      *param_9 = (int)(int *)local_a8;
    }
    return 1;
  }
  FUN_005bfd30(param_1);
  piVar10 = uStack_94._4_4_;
  if (uStack_94._4_4_ != (int *)0x0) {
    (**(code **)(*uStack_94._4_4_ + 0x98))(&local_a8);
    iStack_a0 = 0;
    uStack_9c = 0;
    if ((int *)local_a8 != (int *)0x0) {
      piVar6 = (int *)(**(code **)(*(int *)local_a8 + 8))(local_b0,0);
      iStack_a0 = *piVar6;
      FUN_0040c5f0();
      FUN_0042e230();
    }
    iStack_98 = 0;
    uStack_94 = ZEXT48(uStack_94._4_4_) << 0x20;
    if (iStack_a0 != 0) {
      FUN_0058e280();
      (**(code **)(**(int **)(DAT_00e3d524 + 0xa8) + 4))(&local_b8,auStack_18,&iStack_98,0,4);
      FUN_0041c460();
      if (iStack_98 != 0) {
        piVar6 = *(int **)(iStack_98 + 4);
        local_b4 = piVar6;
        if (piVar6 != (int *)0x0) {
          InterlockedIncrement(piVar6 + 1);
          (**(code **)(*piVar10 + 0x18))(&uStack_48);
          *param_4 = fStack_4c;
          iVar2 = *piVar10;
          uVar7 = iStack_44 - (int)fStack_4c;
          *param_5 = uStack_48;
          uVar8 = iStack_40 - uStack_48;
          cVar5 = (**(code **)(iVar2 + 0x54))(0,4);
          if (cVar5 != '\0') {
            uVar7 = (**(code **)(*piVar6 + 0x48))();
            uVar8 = (**(code **)(*piVar6 + 0x4c))();
            *param_2 = 0;
            *param_3 = 0;
          }
          fVar1 = DAT_00c9d1a0;
          *param_5 = uVar7;
          *param_4 = fVar1;
          *param_6 = uVar8;
          if (((uStack_4 != 0) && (unaff_retaddr != 0)) &&
             ((uStack_4 < uVar7 || (unaff_retaddr < uVar8)))) {
            fVar1 = (float)(int)uVar7;
            if ((int)uVar7 < 0) {
              fVar1 = fVar1 + _DAT_00d0a0dc;
            }
            uStack_94 = CONCAT44(uStack_94._4_4_,fVar1);
            fVar4 = (float)(int)uStack_4;
            if ((int)uStack_4 < 0) {
              fVar4 = fVar4 + _DAT_00d0a0dc;
            }
            fVar12 = (float)(int)uVar8;
            if ((int)uVar8 < 0) {
              fVar12 = fVar12 + _DAT_00d0a0dc;
            }
            fStack_88 = (float)(int)unaff_retaddr;
            if ((int)unaff_retaddr < 0) {
              fStack_88 = fStack_88 + _DAT_00d0a0dc;
            }
            fStack_88 = fStack_88 / fVar12;
            fVar11 = fStack_88;
            if (fVar4 / fVar1 < fStack_88) {
              fVar11 = fVar4 / fVar1;
            }
            *param_4 = fVar11;
            fVar9 = (float10)FUN_004571a0(fVar1 * *param_4);
            fVar1 = *param_4;
            uStack_94 = (longlong)ROUND(fVar9);
            *param_5 = (uint)uStack_94;
            fVar9 = (float10)FUN_004571a0(fVar12 * fVar1);
            _uStack_bc = (ulonglong)ROUND(fVar9);
            *param_6 = (uint)fVar12;
          }
          FUN_009a3ada(auStack_3c,0x18,"%08d_LegacyTileArt",uStack_8);
          FUN_009050c0(*(undefined4 *)(DAT_00e3d540 + 4),auStack_3c,piVar6);
          FUN_00427b70(auStack_3c);
          uStack_84 = *param_2;
          uStack_80 = *param_3;
          uStack_5c = 0xf;
          uStack_60 = 0;
          uStack_70 = 0;
          uStack_7c = uVar7;
          uStack_78 = uVar8;
          FUN_004043d0(param_1,0,0xffffffff);
          _uStack_bc = CONCAT44(local_b8,uStack_8) & 0xffffffff0000ffff;
          uStack_58 = 1;
          FUN_0051e2a0();
          FUN_0051ae70();
          FUN_00403770();
          FUN_00420090();
          FUN_0041c420();
          FUN_0042e230();
          FUN_00449300();
          FUN_0040ca90();
          return 1;
        }
        FUN_00420090();
      }
    }
    FUN_0041c420();
    FUN_0042e230();
    FUN_00449300();
  }
  FUN_0040ca90();
  return 0;
}

```

---

## `FUN_0051e1d0` @ 0051e1d0

- **signature**: `undefined FUN_0051e1d0(void)`
- **triggered by strings**:
  - `s_RequestTileArt_00cae904`
  - `s_ReleaseTileArt_00cae914`
  - `s_RequestLegacyTileArt_00cae924`
  - `s_ReleaseLegacyTileArt_00cae93c`

```c

void FUN_0051e1d0(void)

{
  undefined4 uVar1;
  
  uVar1 = *(undefined4 *)(DAT_00e3d540 + 0xc);
  FUN_00994e1f(uVar1,FUN_0051bff0,"UpdatePortrait");
  FUN_00994e1f(uVar1,FUN_0051c240,"RequestTileArt");
  FUN_00994e1f(uVar1,&LAB_0051c920,"ReleaseTileArt");
  FUN_00994e1f(uVar1,&LAB_0051cac0,"RequestLegacyTileArt");
  FUN_00994e1f(uVar1,&LAB_0051d1a0,"ReleaseLegacyTileArt");
  FUN_00994e1f(uVar1,&LAB_0051d340,"RequestTexture");
  FUN_00994e1f(uVar1,&LAB_0051da20,"ReleaseTexture");
  FUN_00994e1f(uVar1,&LAB_0051dbc0,"RequestGumpArt");
  FUN_00994e1f(uVar1,&LAB_0051e030,"ReleaseGumpArt");
  return;
}

```

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

