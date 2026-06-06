# tileart_enhanced

Auto-generated from `tools/ghidra/ghidra_dump.json`.

Functions discovered via xrefs from strings matching: `TileArtEnhanced, %08d_TileArt, WorldArt, worldart, tileartenhanced`

Total: 6 unique decompiled functions.

---

## `FUN_004604a0` @ 004604a0

- **signature**: `undefined FUN_004604a0(void)`
- **triggered by strings**:
  - `s_Data\WorldArt\_00ca58c4`

```c

void FUN_004604a0(undefined4 param_1)

{
  undefined4 uVar1;
  undefined4 extraout_ECX;
  char *****pppppcVar2;
  undefined4 *unaff_ESI;
  undefined1 auStack_a4 [4];
  char ****appppcStack_a0 [5];
  uint uStack_8c;
  undefined **local_88 [18];
  undefined4 local_40;
  undefined4 local_3c;
  undefined **local_34 [13];
  
  FUN_0058e280();
  *unaff_ESI = _anon_FBC22FCA::WorldArtTextureFileLocation::vftable;
  local_88[0] = &PTR_00ca59fc;
  local_88[2] = (undefined **)&DAT_00ca5a04;
  local_34[0] = std::basic_ios<char,std::char_traits<char>_>::vftable;
  FUN_004644f0(local_88 + 3);
  *(undefined ***)((int)local_88 + (int)local_88[0][1]) =
       std::basic_stringstream<char,std::char_traits<char>,std::allocator<char>_>::vftable;
  FUN_004647e0();
  local_88[3] = std::basic_stringbuf<char,std::char_traits<char>,std::allocator<char>_>::vftable;
  local_40 = 0;
  local_3c = 0;
  uVar1 = FUN_00464f60(local_88 + 2,"Data\\WorldArt\\",extraout_ECX,param_1);
  FUN_00465120(uVar1);
  FUN_00464250(auStack_a4);
  if (uStack_8c < 0x10) {
    appppcStack_a0[0] = (char ****)appppcStack_a0;
  }
  do {
    pppppcVar2 = (char *****)appppcStack_a0[0];
    appppcStack_a0[0] = (char ****)((int)pppppcVar2 + 1);
  } while (*(char *)pppppcVar2 != '\0');
  FUN_0044a330(pppppcVar2);
  FUN_00403770();
  FUN_00463ba0();
  local_34[0] = std::ios_base::vftable;
  FUN_00b6e3fb(local_34);
  return;
}

```

---

## `FUN_004cb850` @ 004cb850

- **signature**: `undefined FUN_004cb850(void)`
- **triggered by strings**:
  - `s_Data\WorldArt\01000045_noise.tga_00caaddc`

```c

undefined4 * FUN_004cb850(undefined4 *param_1,int param_2)

{
  char cVar1;
  char *in_EAX;
  int iVar2;
  char *pcVar3;
  undefined4 uVar4;
  int *local_4;
  
  *param_1 = UOShaderFilenameLegacy::vftable;
  iVar2 = FUN_0047d370(0x2c);
  if (iVar2 == 0) {
    iVar2 = 0;
  }
  else {
    *(undefined4 *)(iVar2 + 0x18) = 0xf;
    *(undefined4 *)(iVar2 + 0x14) = 0;
    *(undefined1 *)(iVar2 + 4) = 0;
    pcVar3 = in_EAX;
    do {
      cVar1 = *pcVar3;
      pcVar3 = pcVar3 + 1;
    } while (cVar1 != '\0');
    FUN_00405e70(in_EAX,(int)pcVar3 - (int)(in_EAX + 1));
    uVar4 = DAT_00c9d1a0;
    *(undefined4 *)(iVar2 + 0x1c) = 0;
    *(undefined4 *)(iVar2 + 0x20) = uVar4;
    *(undefined4 *)(iVar2 + 0x24) = 0;
    *(undefined4 *)(iVar2 + 0x28) = 0;
  }
  param_1[1] = iVar2;
  FUN_0044a3d0();
  FUN_0040c640(iVar2,iVar2);
  iVar2 = FUN_0047d370(0x2c);
  if (iVar2 == 0) {
    iVar2 = 0;
  }
  else {
    *(undefined4 *)(iVar2 + 0x18) = 0xf;
    *(undefined4 *)(iVar2 + 0x14) = 0;
    *(undefined1 *)(iVar2 + 4) = 0;
    FUN_00405e70("Data\\WorldArt\\01000045_noise.tga",0x20);
    uVar4 = DAT_00ca1390;
    *(undefined4 *)(iVar2 + 0x1c) = 0;
    *(undefined4 *)(iVar2 + 0x20) = uVar4;
    *(undefined4 *)(iVar2 + 0x24) = 1;
    *(undefined4 *)(iVar2 + 0x28) = 1;
  }
  param_1[3] = iVar2;
  FUN_0044a3d0();
  FUN_0040c640(iVar2,iVar2);
  param_1[5] = 0;
  param_1[6] = 0;
  if (param_2 != 0) {
    iVar2 = FUN_0047d370(0x2c);
    if (iVar2 == 0) {
      uVar4 = 0;
    }
    else {
      uVar4 = FUN_00449250(0,0x3f800000,0,0);
    }
    FUN_0044a3d0();
    FUN_0040c640(uVar4,uVar4);
    param_1[5] = uVar4;
    FUN_0040c5f0();
    if (local_4 != (int *)0x0) {
      LOCK();
      iVar2 = local_4[1] + -1;
      local_4[1] = iVar2;
      UNLOCK();
      if (iVar2 == 0) {
        (**(code **)(*local_4 + 4))();
        LOCK();
        iVar2 = local_4[2] + -1;
        local_4[2] = iVar2;
        UNLOCK();
        if (iVar2 == 0) {
          (**(code **)(*local_4 + 8))();
        }
      }
    }
  }
  return param_1;
}

```

---

## `FUN_0051a840` @ 0051a840

- **signature**: `undefined FUN_0051a840(void)`
- **triggered by strings**:
  - `s_%08d_TileArt_00cae79c`

```c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4
FUN_0051a840(float param_1,uint param_2,undefined4 *param_3,undefined4 *param_4,float *param_5,
            float *param_6,float *param_7,uint *param_8,int *param_9)

{
  uint uVar1;
  int iVar2;
  float fVar3;
  float fVar4;
  float fVar5;
  float fVar6;
  char cVar7;
  float *pfVar8;
  int *piVar9;
  int *piVar10;
  float fVar11;
  float fVar12;
  undefined2 in_FPUControlWord;
  float10 fVar13;
  float unaff_retaddr;
  undefined8 local_a8;
  undefined4 *local_a0 [2];
  longlong local_98;
  int *local_8c;
  int local_88;
  int local_84;
  undefined4 local_80;
  int local_7c [2];
  float *local_74;
  longlong local_70;
  undefined4 uStack_68;
  undefined4 uStack_64;
  float fStack_60;
  float fStack_5c;
  undefined1 uStack_54;
  undefined4 uStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined1 local_30 [16];
  float fStack_20;
  float fStack_1c;
  undefined4 uStack_4;
  
  local_a8 = CONCAT44(param_1,(float)local_a8) & 0xffffffffffff;
  FUN_0051e6c0((int)&local_a8 + 4);
  if ((float)local_a8 != (float)DAT_00e3a068) {
    *(int *)((int)(float)local_a8 + 0x3c) = *(int *)((int)(float)local_a8 + 0x3c) + 1;
    fVar3 = DAT_00c9d1a0;
    *param_5 = *(float *)((int)(float)local_a8 + 0x10);
    *param_6 = *(float *)((int)(float)local_a8 + 0x14);
    uVar1 = *(uint *)((int)(float)local_a8 + 0x18);
    *param_9 = *(int *)((int)(float)local_a8 + 0x1c);
    *param_8 = uVar1;
    *param_7 = fVar3;
    FUN_004043d0((int)(float)local_a8 + 0x20,0,0xffffffff);
    if (((param_2 != 0) && (param_3 != (undefined4 *)0x0)) &&
       ((uVar1 = *param_8, param_2 < uVar1 || (param_3 < (undefined4 *)*param_9)))) {
      fVar3 = (float)(int)uVar1;
      if ((int)uVar1 < 0) {
        fVar3 = fVar3 + _DAT_00d0a0dc;
      }
      fVar11 = (float)(int)param_2;
      if ((int)param_2 < 0) {
        fVar11 = fVar11 + _DAT_00d0a0dc;
      }
      fVar11 = fVar11 / fVar3;
      local_a0[0] = param_3;
      fVar12 = (float)(int)param_3;
      if ((int)param_3 < 0) {
        fVar12 = fVar12 + _DAT_00d0a0dc;
      }
      fVar4 = (float)*param_9;
      if (*param_9 < 0) {
        fVar4 = fVar4 + _DAT_00d0a0dc;
      }
      fVar12 = fVar12 / fVar4;
      local_a8 = CONCAT44(fVar11,fVar12);
      if (fVar11 < fVar12) {
        fVar12 = fVar11;
      }
      *param_7 = fVar12;
      fVar13 = (float10)FUN_00457180(fVar3 * *param_7);
      iVar2 = *param_9;
      local_a8 = CONCAT62(local_a8._2_6_,in_FPUControlWord);
      local_a8 = (ulonglong)CONCAT24(in_FPUControlWord,(float)local_a8) | 0xc0000000000;
      local_98 = (longlong)ROUND(fVar13);
      *param_8 = (uint)local_98;
      fVar3 = (float)*param_9;
      if (iVar2 < 0) {
        fVar3 = fVar3 + _DAT_00d0a0dc;
      }
      fVar13 = (float10)FUN_00457180(fVar3 * *param_7);
      local_98._0_4_ = (uint)(longlong)ROUND(fVar13);
      *param_9 = (uint)local_98;
    }
    return 1;
  }
  FUN_005bfd30(param_1);
  if (local_8c != (int *)0x0) {
    if (local_88 != 0) {
      LOCK();
      *(int *)(local_88 + 4) = *(int *)(local_88 + 4) + 1;
      UNLOCK();
    }
    pfVar8 = (float *)FUN_00457b20(0,local_8c,local_88);
    local_74 = pfVar8;
    FUN_0051fb60();
    FUN_0040c640(pfVar8,pfVar8);
    pfVar8 = local_74;
    piVar10 = (int *)local_74[6];
    local_98 = *(longlong *)(local_74 + 6);
    if (local_74[7] != 0.0) {
      piVar9 = (int *)((int)local_74[7] + 4);
      LOCK();
      *piVar9 = *piVar9 + 1;
      UNLOCK();
    }
    local_84 = 0;
    local_80 = 0;
    if (piVar10 != (int *)0x0) {
      piVar10 = (int *)(**(code **)(*piVar10 + 8))(local_a0,0);
      local_84 = *piVar10;
      FUN_0040c5f0();
      FUN_0042e230();
    }
    local_7c[0] = 0;
    local_7c[1] = 0;
    if (local_84 != 0) {
      FUN_0058e280();
      (**(code **)(**(int **)(DAT_00e3d524 + 0xa8) + 4))(&local_a8,local_30,local_7c,0,4);
      FUN_0041c460();
      if (local_7c[0] != 0) {
        piVar10 = *(int **)(local_7c[0] + 4);
        local_a8 = CONCAT44(piVar10,(float)local_a8);
        if (piVar10 != (int *)0x0) {
          InterlockedIncrement(piVar10 + 1);
          fVar3 = *pfVar8;
          fStack_20 = pfVar8[4];
          fStack_1c = pfVar8[5];
          fVar12 = (float)((int)pfVar8[3] - (int)pfVar8[1]);
          fVar11 = (float)((int)pfVar8[2] - (int)fVar3);
          *param_6 = pfVar8[1];
          *param_5 = fVar3;
          cVar7 = (**(code **)(*local_8c + 0x54))(0,4);
          if (cVar7 != '\0') {
            fVar11 = (float)(**(code **)(*piVar10 + 0x48))();
            fVar12 = (float)(**(code **)(*piVar10 + 0x4c))();
            *param_3 = 0;
            *param_4 = 0;
          }
          fVar3 = DAT_00c9d1a0;
          *param_6 = fVar11;
          *param_5 = fVar3;
          *param_7 = fVar12;
          if (((unaff_retaddr != 0.0) && (param_1 != 0.0)) &&
             (((uint)unaff_retaddr < (uint)fVar11 || ((uint)param_1 < (uint)fVar12)))) {
            fVar3 = (float)(int)fVar11;
            if ((int)fVar11 < 0) {
              fVar3 = fVar3 + _DAT_00d0a0dc;
            }
            local_70 = CONCAT44(local_70._4_4_,fVar3);
            fVar4 = (float)(int)unaff_retaddr;
            if ((int)unaff_retaddr < 0) {
              fVar4 = fVar4 + _DAT_00d0a0dc;
            }
            fVar5 = (float)(int)fVar12;
            if ((int)fVar12 < 0) {
              fVar5 = fVar5 + _DAT_00d0a0dc;
            }
            local_a8 = CONCAT44(local_a8._4_4_,fVar5);
            fVar6 = (float)(int)param_1;
            if ((int)param_1 < 0) {
              fVar6 = fVar6 + _DAT_00d0a0dc;
            }
            local_74 = (float *)(fVar6 / fVar5);
            pfVar8 = local_74;
            if (fVar4 / fVar3 < (float)local_74) {
              pfVar8 = (float *)(fVar4 / fVar3);
            }
            *param_5 = (float)pfVar8;
            fVar13 = (float10)FUN_004571a0(fVar3 * *param_5);
            fVar3 = *param_5;
            local_70 = (longlong)ROUND(fVar13);
            *param_6 = (float)local_70;
            fVar13 = (float10)FUN_004571a0((float)local_a8 * fVar3);
            local_a8 = (ulonglong)ROUND(fVar13);
            *param_7 = (float)local_a8;
          }
          FUN_009a3ada(&fStack_20,0x18,"%08d_TileArt",uStack_4);
          FUN_009050c0(*(undefined4 *)(DAT_00e3d540 + 4),&fStack_20,piVar10);
          FUN_00427b70(&fStack_20);
          uStack_68 = *param_3;
          uStack_64 = *param_4;
          uStack_40 = 0xf;
          uStack_44 = 0;
          uStack_54 = 0;
          fStack_60 = fVar11;
          fStack_5c = fVar12;
          FUN_004043d0(param_2,0,0xffffffff);
          local_a8 = CONCAT44(local_a8._4_4_,uStack_4) & 0xffffffff0000ffff;
          uStack_3c = 1;
          FUN_0051e2a0();
          FUN_0051ae70();
          FUN_00403770();
          FUN_00420090();
          FUN_0041c420();
          FUN_0042e230();
          FUN_00449300();
          FUN_0051ae30();
          FUN_0040ca90();
          return 1;
        }
        FUN_00420090();
      }
    }
    FUN_0041c420();
    FUN_0042e230();
    FUN_00449300();
    FUN_0051ae30();
  }
  FUN_0040ca90();
  return 0;
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

