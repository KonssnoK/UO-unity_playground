# terrain

Auto-generated from `tools/ghidra/ghidra_dump.json`.

Functions discovered via xrefs from strings matching: `Terrain, AtlasTerrain, GameTerrain, UOStaticTerrain, LegacyTerrain, TerrainDefinition, TerrainTexture, UOTerrainCollision, UOTerrainTexturingProperty, UOWaterTerrainLayer, UODefaultTerrainLayer, UOBumpMapTerrainLayer`

Total: 20 unique decompiled functions.

---

## `FUN_00415350` @ 00415350

- **signature**: `undefined FUN_00415350(void)`
- **triggered by strings**:
  - `PTR_s_UOTerrainCollisionNode_00dc3268`

```c

undefined ** FUN_00415350(void)

{
  return &PTR_s_UOTerrainCollisionNode_00dc3268;
}

```

---

## `FUN_004600d0` @ 004600d0

- **signature**: `undefined FUN_004600d0(void)`
- **triggered by strings**:
  - `PTR_s_TerrainTriShape_00dc7b20`

```c

undefined ** FUN_004600d0(void)

{
  return &PTR_s_TerrainTriShape_00dc7b20;
}

```

---

## `FUN_004602f0` @ 004602f0

- **signature**: `undefined FUN_004602f0(void)`
- **triggered by strings**:
  - `PTR_s_UOTerrainTexturingProperty_00dd60a0`

```c

undefined ** FUN_004602f0(void)

{
  return &PTR_s_UOTerrainTexturingProperty_00dd60a0;
}

```

---

## `FUN_00461790` @ 00461790

- **signature**: `undefined FUN_00461790(void)`
- **triggered by strings**:
  - `s_UOTerrainShader_00ca5878`
  - `s_UOWaterTerrainLayer_00ca58e4`
  - `s_UODefaultTerrainLayer_00ca58f8`
  - `s_UOBumpMapTerrainLayer_00ca5910`

```c

int FUN_00461790(void)

{
  char cVar1;
  int iVar2;
  undefined4 in_stack_00000018;
  
  iVar2 = FUN_004229a0(0,in_stack_00000018,"UOWaterTerrainLayer",0x13);
  if (iVar2 == 0) {
LAB_00461860:
    iVar2 = FUN_0047d370(0x38);
    if (iVar2 != 0) {
      iVar2 = FUN_00460240();
LAB_00461875:
      if (iVar2 != 0) goto LAB_004618a2;
    }
  }
  else {
    iVar2 = FUN_004229a0(0,in_stack_00000018,"UODefaultTerrainLayer",0x15);
    if (iVar2 == 0) {
      iVar2 = FUN_0047d370(0x38);
      if (iVar2 != 0) {
        iVar2 = FUN_00598380();
        goto LAB_00461875;
      }
    }
    else {
      iVar2 = FUN_004229a0(0,in_stack_00000018,"UOBumpMapTerrainLayer",0x15);
      if (iVar2 == 0) {
        iVar2 = FUN_0047d370(0x38);
        if (iVar2 != 0) {
          iVar2 = FUN_004601a0();
          goto LAB_00461875;
        }
      }
      else {
        iVar2 = FUN_004229a0(0,in_stack_00000018,"UOTerrainShader",0xf);
        if (iVar2 == 0) {
          iVar2 = FUN_0047d370(0x38);
          if (iVar2 != 0) {
            iVar2 = FUN_00598380();
            goto LAB_00461875;
          }
        }
        else {
          cVar1 = FUN_0045c370();
          if (cVar1 != '\0') goto LAB_00461860;
        }
      }
    }
  }
  iVar2 = FUN_0047d370(0x38);
  if (iVar2 != 0) {
    iVar2 = FUN_00598380();
    FUN_00403770();
    return iVar2;
  }
  iVar2 = 0;
LAB_004618a2:
  FUN_00403770();
  return iVar2;
}

```

---

## `FUN_00461bc0` @ 00461bc0

- **signature**: `undefined FUN_00461bc0(void)`
- **triggered by strings**:
  - `s_UOTerrainShader_00ca5878`

```c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00461bc0(int *param_1)

{
  int *piVar1;
  int *piVar2;
  float fVar3;
  undefined *puVar4;
  int **ppiVar5;
  int *piVar6;
  int *piVar7;
  float *pfVar8;
  int iVar9;
  undefined4 *puVar10;
  uint uVar11;
  undefined4 *puVar12;
  undefined **ppuVar13;
  LONG LVar14;
  int *piVar15;
  float unaff_EBX;
  float unaff_EBP;
  int *unaff_ESI;
  undefined **ppuVar16;
  LONG *unaff_EDI;
  float *pfVar17;
  LONG *pLVar18;
  float fVar19;
  float fVar20;
  undefined4 uVar21;
  int *piStack_1bc;
  float fStack_1b8;
  int *piStack_1b4;
  undefined **ppuVar22;
  undefined **ppuStack_1a8;
  undefined4 *puStack_1a4;
  int **ppiStack_1a0;
  int *piStack_19c;
  int *piStack_198;
  int *piStack_194;
  float fStack_190;
  undefined ***pppuStack_18c;
  undefined4 *puStack_17c;
  float fStack_178;
  int *piStack_174;
  int **ppiStack_170;
  float *pfStack_16c;
  float fStack_154;
  int iStack_150;
  int *piStack_14c;
  undefined **ppuStack_148;
  undefined4 *puStack_144;
  int *piStack_140;
  float fStack_13c;
  int iStack_138;
  float fStack_134;
  int *piStack_130;
  undefined4 uStack_12c;
  int *piStack_128;
  float fStack_124;
  float fStack_11c;
  float fStack_118;
  float fStack_114;
  int *piStack_110;
  float fStack_10c;
  undefined4 *puStack_108;
  undefined4 uStack_104;
  LONG *pLStack_100;
  LONG *pLStack_fc;
  LONG *pLStack_f8;
  LONG *pLStack_f4;
  float fStack_f0;
  LONG *pLStack_ec;
  float fStack_e8;
  float fStack_e4;
  LONG *apLStack_e0 [2];
  float fStack_d8;
  undefined **ppuStack_d4;
  float fStack_d0;
  float fStack_c8;
  float fStack_c4;
  float fStack_c0;
  float fStack_bc;
  float fStack_b8;
  float fStack_b4;
  float fStack_b0;
  undefined ***pppuStack_ac;
  undefined1 auStack_a8 [40];
  int **ppiStack_80;
  float fStack_7c;
  int *piStack_78;
  
  piVar15 = param_1 + 0x3006;
  (**(code **)(param_1[0x3006] + 0x14))();
  (**(code **)(param_1[0x300a] + 0x14))();
  (**(code **)(param_1[0x300e] + 0x14))();
  (**(code **)(param_1[0x3012] + 0x14))();
  piVar2 = param_1 + 0x3016;
  (**(code **)(param_1[0x3016] + 0xc))();
  puStack_108 = (undefined4 *)FUN_00440620();
  *(undefined1 *)((int)puStack_108 + 0x11) = 1;
  puStack_108[1] = puStack_108;
  *puStack_108 = puStack_108;
  puStack_108[2] = puStack_108;
  uStack_104 = 0;
  piVar7 = (int *)**(int **)(param_1[5] + 0x1600c);
  if (piVar7 != *(int **)(param_1[5] + 0x1600c)) {
    do {
      iVar9 = piVar7[2];
      pfStack_16c = &fStack_114;
      ppiStack_170 = (int **)0x461c82;
      FUN_004cc3f0();
      if (fStack_114 != 0.0) {
        for (piVar6 = *(int **)((int)fStack_114 + 8); piVar6 != *(int **)((int)fStack_114 + 0xc);
            piVar6 = piVar6 + 8) {
          if (*piVar6 == 0) goto LAB_00461ca5;
        }
        piVar6 = (int *)0x0;
LAB_00461ca5:
        if ((piVar6[3] & 2U) == 2) {
          pfStack_16c = &fStack_10c;
          ppiStack_170 = (int **)0x461ccb;
          piStack_140 = (int *)iVar9;
          FUN_0043b2e0();
        }
      }
      piVar6 = piStack_110;
      if (piStack_110 != (int *)0x0) {
        LOCK();
        iVar9 = piStack_110[1] + -1;
        piStack_110[1] = iVar9;
        UNLOCK();
        if (iVar9 == 0) {
          (**(code **)(*piStack_110 + 4))();
          piVar1 = piVar6 + 2;
          LOCK();
          iVar9 = *piVar1 + -1;
          *piVar1 = iVar9;
          UNLOCK();
          if (iVar9 == 0) {
            (**(code **)(*piVar6 + 8))();
          }
        }
      }
      piVar7 = (int *)*piVar7;
    } while (piVar7 != (int *)*(int *)(param_1[5] + 0x1600c));
  }
  puStack_144 = puStack_108;
  piStack_14c = (int *)0x0;
  do {
    piStack_140 = (int *)((int)piStack_14c * 0xb00);
    iStack_150 = 0;
    pfVar17 = (float *)(param_1 + (int)piStack_14c * 0x180 + 0xb);
    do {
      ppuStack_148 = (undefined **)(uint)*(byte *)((int)piStack_140 + param_1[5] + 0x20);
      pfStack_16c = (float *)0x461d76;
      piVar7 = (int *)FUN_0043b3c0();
      if ((undefined4 *)*piVar7 == puStack_144) {
        ppuStack_148 = (undefined **)(**(code **)(*piVar15 + 0x18))();
        pfStack_16c = (float *)0x461d99;
        (**(code **)(*piVar2 + 4))();
        pfStack_16c = (float *)((int)piStack_14c + 2);
        ppiStack_170 = (int **)0x461daa;
        (**(code **)(*piVar2 + 4))();
        ppiStack_170 = (int **)(iStack_150 + 1);
        piStack_174 = (int *)0x461dbb;
        (**(code **)(*piVar2 + 4))();
        piStack_174 = (int *)((int)fStack_154 + 1);
        fStack_178 = 6.439174e-39;
        (**(code **)(*piVar2 + 4))();
        fStack_178 = (float)((int)unaff_EBX + 2);
        puStack_17c = (undefined4 *)0x461ddd;
        (**(code **)(*piVar2 + 4))();
        puStack_17c = (undefined4 *)((int)unaff_EBP + 3);
        (**(code **)(*piVar2 + 4))();
        fStack_c0 = pfVar17[-5] + (float)param_1[2];
        fStack_bc = pfVar17[-4] + (float)param_1[3];
        fStack_b8 = pfVar17[-3] + (float)param_1[4];
        pppuStack_18c = (undefined ***)0x461e52;
        (**(code **)(*piVar15 + 4))();
        piStack_194 = (int *)(pfVar17[-2] + (float)param_1[2]);
        fStack_190 = pfVar17[-1] + (float)param_1[3];
        pppuStack_18c = (undefined ***)((float)param_1[4] + *pfVar17);
        piStack_198 = (int *)0x461eb5;
        fStack_b4 = (float)piStack_194;
        fStack_b0 = fStack_190;
        pppuStack_ac = pppuStack_18c;
        (**(code **)(*piVar15 + 4))();
        ppiStack_1a0 = (int **)(pfVar17[1] + (float)param_1[2]);
        piStack_19c = (int *)(pfVar17[2] + (float)param_1[3]);
        piStack_198 = (int *)(pfVar17[3] + (float)param_1[4]);
        puStack_1a4 = (undefined4 *)0x461f19;
        ppiStack_80 = ppiStack_1a0;
        fStack_7c = (float)piStack_19c;
        piStack_78 = piStack_198;
        (**(code **)(*piVar15 + 4))();
        fVar19 = pfVar17[4];
        fVar3 = (float)param_1[2];
        ppuStack_1a8 = (undefined **)(pfVar17[5] + (float)param_1[3]);
        puStack_1a4 = (undefined4 *)(pfVar17[6] + (float)param_1[4]);
        fStack_d8 = fVar19 + fVar3;
        ppuStack_d4 = ppuStack_1a8;
        fStack_d0 = (float)puStack_1a4;
        (**(code **)(*piVar15 + 4))();
        piStack_1b4 = (int *)(float)(*param_1 + (int)piStack_198);
        fVar20 = DAT_00d0a160 - (float)(param_1[1] + (int)piStack_194);
        fStack_1b8 = 6.4399e-39;
        piStack_128 = piStack_1b4;
        fStack_124 = fVar20;
        (**(code **)(param_1[0x300e] + 4))();
        piStack_1bc = (int *)((float)(*param_1 + (int)ppiStack_1a0) + (float)DAT_00c9d1a0);
        fStack_1b8 = DAT_00d0a160 - (float)(param_1[1] + (int)piStack_19c);
        piStack_140 = piStack_1bc;
        fStack_13c = fStack_1b8;
        (**(code **)(param_1[0x300e] + 4))();
        piStack_194 = (int *)(float)(*param_1 + (int)ppuStack_1a8);
        fStack_190 = DAT_00d0a160 - ((float)(param_1[1] + (int)puStack_1a4) + (float)DAT_00c9d1a0);
        (**(code **)(param_1[0x300e] + 4))(piStack_194,fStack_190);
        fStack_c8 = (float)(*param_1 + (int)fVar20) + (float)DAT_00c9d1a0;
        fStack_c4 = DAT_00d0a160 -
                    ((float)(param_1[1] + (int)(fVar19 + fVar3)) + (float)DAT_00c9d1a0);
        (**(code **)(param_1[0x300e] + 4))(fStack_c8,fStack_c4);
        piStack_194 = (int *)((float)(int)fStack_1b8 * DAT_00d0a214);
        piStack_19c = (int *)((float)(int)piStack_1b4 * DAT_00d0a214);
        fStack_134 = (float)piStack_194;
        piStack_130 = piStack_19c;
        (**(code **)(param_1[0x3012] + 4))(piStack_194,piStack_19c);
        fStack_154 = (float)puStack_1a4;
        puVar10 = puStack_1a4;
        (**(code **)(param_1[0x3012] + 4))
                  (((float)pppuStack_18c + (float)DAT_00c9d1a0) * DAT_00d0a214,puStack_1a4);
        fStack_178 = (float)puStack_1a4;
        piStack_174 = (int *)((fStack_190 + (float)DAT_00c9d1a0) * DAT_00d0a214);
        pfStack_16c = (float *)piStack_174;
        (**(code **)(param_1[0x3012] + 4))(puStack_1a4,piStack_174);
        piStack_194 = (int *)fStack_178;
        fStack_190 = (float)piStack_174;
        piVar7 = piStack_174;
        (**(code **)(param_1[0x3012] + 4))(fStack_178,piStack_174);
        pfVar8 = (float *)FUN_00460d20(&fStack_bc,puVar10);
        unaff_ESI = (int *)*pfVar8;
        unaff_EBP = pfVar8[1];
        unaff_EBX = pfVar8[2];
        pLVar18 = (LONG *)((unaff_EBP * _DAT_00dc7b2c + unaff_EBX * _DAT_00dc7b30 +
                            (float)unaff_ESI * _DAT_00dc7b28 + (float)DAT_00c9d1a0) * DAT_00c9a604);
        pLStack_f4 = DAT_00c9d1a0;
        pLStack_100 = pLVar18;
        pLStack_fc = pLVar18;
        pLStack_f8 = pLVar18;
        (**(code **)(param_1[0x300a] + 4))(pLVar18,pLVar18,pLVar18,DAT_00c9d1a0);
        pfVar8 = (float *)FUN_00460d20(auStack_a8,(int)piVar7 + 1);
        fStack_11c = *pfVar8;
        fStack_118 = pfVar8[1];
        fStack_114 = pfVar8[2];
        fVar19 = (fStack_118 * _DAT_00dc7b2c + fStack_114 * _DAT_00dc7b30 +
                  fStack_11c * _DAT_00dc7b28 + (float)DAT_00c9d1a0) * DAT_00c9a604;
        pLStack_ec = DAT_00c9d1a0;
        pLStack_f8 = (LONG *)fVar19;
        pLStack_f4 = (LONG *)fVar19;
        fStack_f0 = fVar19;
        (**(code **)(param_1[0x300a] + 4))(fVar19,fVar19,fVar19,DAT_00c9d1a0);
        pfVar8 = (float *)FUN_00460d20(&fStack_c4,pLVar18);
        pfStack_16c = (float *)*pfVar8;
        pLStack_ec = (LONG *)((pfVar8[1] * _DAT_00dc7b2c + pfVar8[2] * _DAT_00dc7b30 +
                               (float)pfStack_16c * _DAT_00dc7b28 + (float)DAT_00c9d1a0) *
                             DAT_00c9a604);
        apLStack_e0[0] = DAT_00c9d1a0;
        fStack_e8 = (float)pLStack_ec;
        fStack_e4 = (float)pLStack_ec;
        (**(code **)(param_1[0x300a] + 4))(pLStack_ec,pLStack_ec,pLStack_ec,DAT_00c9d1a0);
        pfVar8 = (float *)FUN_00460d20(apLStack_e0,(int)fVar19 + 1);
        unaff_EDI = DAT_00c9d1a0;
        ppiStack_170 = (int **)((pfVar8[1] * _DAT_00dc7b2c + pfVar8[2] * _DAT_00dc7b30 +
                                 *pfVar8 * _DAT_00dc7b28 + (float)DAT_00c9d1a0) * DAT_00c9a604);
        pfStack_16c = (float *)ppiStack_170;
        (**(code **)(param_1[0x300a] + 4))(ppiStack_170,ppiStack_170,ppiStack_170,DAT_00c9d1a0);
      }
      piStack_140 = piStack_140 + 0x16;
      iStack_150 = iStack_150 + 1;
      pfVar17 = pfVar17 + 0xc;
    } while (iStack_150 < 0x20);
    piStack_14c = (int *)((int)piStack_14c + 1);
  } while ((int)piStack_14c < 0x20);
  iVar9 = (**(code **)(*piVar15 + 0x18))();
  if (iVar9 == 0) {
    pfStack_16c = (float *)*puStack_108;
    ppiStack_170 = &piStack_130;
    piStack_174 = (int *)0x4625f3;
    FUN_0043e5b0();
  }
  else {
    fStack_134 = (float)(**(code **)(*piVar15 + 0xc))();
    uStack_12c = (**(code **)(param_1[0x300a] + 0xc))();
    puStack_144 = (undefined4 *)(**(code **)(*piVar2 + 8))();
    pfStack_16c = (float *)0x462643;
    (**(code **)(param_1[0x300e] + 0x10))();
    pfStack_16c = (float *)0x46264c;
    fStack_11c = (float)(**(code **)(param_1[0x300e] + 0xc))();
    pfStack_16c = (float *)0x0;
    ppiStack_170 = (int **)0xffffffff;
    piStack_174 = (int *)0x0;
    fStack_178 = 1.4013e-45;
    puStack_17c = (undefined4 *)0x1;
    pLStack_f8 = (LONG *)0x4;
    pLStack_fc = (LONG *)0x5c;
    puVar10 = (undefined4 *)(**(code **)(*(int *)*DAT_00e381e0 + 4))();
    if (puVar10 == (undefined4 *)0x0) {
      pppuStack_18c = (undefined ***)&PTR_s_bad_allocation_00dc1bcc;
      fStack_190 = 6.442353e-39;
      FUN_00b70479();
      pppuStack_18c = &ppuStack_148;
      ppuStack_148 = std::bad_alloc::vftable;
                    /* WARNING: Subroutine does not return */
      fStack_190 = 6.442386e-39;
      __CxxThrowException_8();
    }
    uVar11 = (**(code **)(*piVar2 + 0x10))();
    fStack_13c = (float)(uVar11 / 3 & 0xffff);
    (**(code **)(*piVar15 + 0x18))();
    pppuStack_18c = (undefined ***)0x2;
    fStack_190 = (float)iStack_138;
    piStack_194 = piStack_14c;
    piStack_198 = (int *)0x0;
    piStack_19c = (int *)fStack_154;
    ppiStack_1a0 = (int **)0x462703;
    FUN_0068cce0();
    *(short *)(puVar10 + 0x11) = SUB42(fStack_13c,0);
    *(short *)((int)puVar10 + 0x46) = SUB42(fStack_13c,0);
    puVar10[0x13] = unaff_EDI;
    pLStack_100 = puVar10 + 1;
    *puVar10 = &PTR_FUN_00cc5128;
    puVar10[0x12] = ((uint)fStack_13c & 0xffff) * 3;
    puVar10[0x14] = 0;
    *(undefined2 *)(puVar10 + 0x15) = 0;
    puVar10[0x16] = 0;
    pppuStack_18c = (undefined ***)0x462740;
    InterlockedIncrement(pLStack_100);
    pppuStack_18c = (undefined ***)0xffffffff;
    fStack_190 = 0.0;
    piStack_194 = (int *)0x1;
    piStack_198 = (int *)0x1;
    piStack_19c = &iStack_138;
    iStack_138 = 4;
    piStack_14c = (int *)0xe4;
    ppiStack_1a0 = &piStack_14c;
    puStack_1a4 = (undefined4 *)0x462771;
    puVar12 = (undefined4 *)(**(code **)(*(int *)*DAT_00e381e0 + 4))();
    puStack_17c = puVar12;
    if (puVar12 == (undefined4 *)0x0) {
      puStack_1a4 = (undefined4 *)0x1;
      ppuStack_1a8 = &PTR_s_bad_allocation_00dc1bcc;
      FUN_00b70479();
      puStack_1a4 = (undefined4 *)&DAT_00d42574;
      ppuStack_1a8 = (undefined **)&stack0xfffffe9c;
                    /* WARNING: Subroutine does not return */
      __CxxThrowException_8();
    }
    ppuStack_1a8 = (undefined **)0x4627aa;
    puStack_1a4 = puVar10;
    FUN_0066a680();
    piVar15 = DAT_00e38300;
    _DAT_00e3808c = _DAT_00e3808c + 1;
    puStack_1a4 = (undefined4 *)0x1;
    *puVar12 = TerrainTriShape::vftable;
    puVar12[0x2d] = 1;
    ppuStack_1a8 = (undefined **)0x0;
    (**(code **)(*piVar15 + 8))();
    piStack_1b4 = (int *)0x4627e2;
    EnterCriticalSection((LPCRITICAL_SECTION)&DAT_00e39414);
    piStack_1b4 = (int *)0x4627ea;
    FUN_006a20d0();
    piStack_1b4 = (int *)0x4627f8;
    FUN_0066abd0();
    piStack_1b4 = (int *)0x462803;
    LeaveCriticalSection((LPCRITICAL_SECTION)&DAT_00e39414);
    piStack_1b4 = (int *)0xffffffff;
    fStack_1b8 = 0.0;
    piStack_1bc = (int *)0x1;
    uVar21 = 1;
    puStack_17c = (undefined4 *)0x4;
    ppuVar13 = (undefined **)
               (**(code **)(*(int *)*DAT_00e381e0 + 4))(&stack0xfffffe9c,&puStack_17c,1);
    if (ppuVar13 == (undefined **)0x0) {
      FUN_00b70479(&PTR_s_bad_allocation_00dc1bcc,1);
      pppuStack_18c = (undefined ***)std::bad_alloc::vftable;
                    /* WARNING: Subroutine does not return */
      __CxxThrowException_8(&pppuStack_18c,&DAT_00d42574);
    }
    ppuVar22 = ppuVar13;
    FUN_00674a60();
    *ppuVar13 = (undefined *)UOTerrainTexturingProperty::vftable;
    ppuVar16 = ppuVar13 + 1;
    ppuVar13[0xe] = (undefined *)0x0;
    ppuVar13[0xf] = (undefined *)0x0;
    ppuVar13[0x10] = (undefined *)0x0;
    InterlockedIncrement((LONG *)ppuVar16);
    *(ushort *)(ppuVar13 + 6) = *(ushort *)(ppuVar13 + 6) & 0xfff1;
    ppuStack_1a8 = ppuVar13;
    InterlockedIncrement((LONG *)ppuVar16);
    FUN_00418a20(&ppuStack_1a8);
    LVar14 = InterlockedDecrement((LONG *)ppuVar16);
    if (LVar14 == 0) {
      (**(code **)(*ppuVar13 + 4))();
    }
    piStack_1b4 = (int *)**(int **)(param_1[5] + 0x1600c);
    ppuVar16 = ppuVar13;
    if (piStack_1b4 != *(int **)(param_1[5] + 0x1600c)) {
      do {
        ppuVar16 = ppuVar22;
        FUN_004cc3f0(&ppiStack_1a0,piStack_1b4[2]);
        ppiVar5 = ppiStack_1a0;
        piVar15 = ppiStack_1a0[0x11];
        piStack_14c = ppiStack_1a0[0x10];
        if (piVar15 != (int *)0x0) {
          piVar2 = piVar15 + 1;
          LOCK();
          *piVar2 = *piVar2 + 1;
          UNLOCK();
          LOCK();
          iVar9 = *piVar2;
          *piVar2 = iVar9 + -1;
          UNLOCK();
          if (iVar9 + -1 == 0) {
            (**(code **)(*piVar15 + 4))();
            LOCK();
            iVar9 = piVar15[2] + -1;
            piVar15[2] = iVar9;
            UNLOCK();
            if (iVar9 == 0) {
              (**(code **)(*piVar15 + 8))();
            }
          }
        }
        piVar15 = piStack_19c;
        if (piStack_14c == (int *)0x0) {
          if (piStack_19c != (int *)0x0) {
            LOCK();
            iVar9 = piStack_19c[1] + -1;
            piStack_19c[1] = iVar9;
            UNLOCK();
            if (iVar9 == 0) {
              (**(code **)(*piStack_19c + 4))();
              LOCK();
              iVar9 = piVar15[2] + -1;
              piVar15[2] = iVar9;
              UNLOCK();
              if (iVar9 == 0) {
                iVar9 = *piVar15;
LAB_00462abf:
                (**(code **)(iVar9 + 8))();
              }
            }
          }
        }
        else {
          if (piStack_19c != (int *)0x0) {
            LOCK();
            piStack_19c[1] = piStack_19c[1] + 1;
            UNLOCK();
          }
          FUN_004618b0(&stack0xfffffe9c,param_1[5],ppiVar5,piStack_19c);
          if (unaff_ESI != (int *)0x0) {
            LOCK();
            unaff_ESI[1] = unaff_ESI[1] + 1;
            UNLOCK();
          }
          puVar4 = ppuVar13[0xe];
          fStack_178 = 9.52883e-44;
          piStack_174 = unaff_ESI;
          if ((puVar4 == (undefined *)0x0) ||
             ((uint)((int)ppuVar13[0x10] - (int)puVar4 >> 3) <=
              (uint)((int)ppuVar13[0xf] - (int)puVar4 >> 3))) {
            FUN_004649d0(ppuVar13 + 0xd,ppuVar13[0xf],&fStack_178);
          }
          else {
            puVar4 = ppuVar13[0xf];
            ppuStack_1a8 = (undefined **)((uint)ppuStack_1a8 & 0xffffff00);
            FUN_00465590(puVar4,1,&fStack_178,piStack_194,ppuStack_1a8);
            ppuVar13[0xf] = puVar4 + 8;
            piVar15 = piStack_19c;
          }
          if (unaff_ESI != (int *)0x0) {
            piVar15 = unaff_ESI + 1;
            LOCK();
            iVar9 = *piVar15;
            *piVar15 = iVar9 + -1;
            UNLOCK();
            if (iVar9 + -1 == 0) {
              (**(code **)(*unaff_ESI + 4))();
              LOCK();
              iVar9 = unaff_ESI[2] + -1;
              unaff_ESI[2] = iVar9;
              UNLOCK();
              if (iVar9 == 0) {
                (**(code **)(*unaff_ESI + 8))();
              }
            }
            LOCK();
            iVar9 = *piVar15;
            *piVar15 = iVar9 + -1;
            UNLOCK();
            piVar15 = piStack_19c;
            if (iVar9 + -1 == 0) {
              (**(code **)(*unaff_ESI + 4))();
              LOCK();
              iVar9 = unaff_ESI[2] + -1;
              unaff_ESI[2] = iVar9;
              UNLOCK();
              piVar15 = piStack_19c;
              if (iVar9 == 0) {
                (**(code **)(*unaff_ESI + 8))();
                piVar15 = piStack_19c;
              }
            }
          }
          if (piVar15 != (int *)0x0) {
            LOCK();
            iVar9 = piVar15[1] + -1;
            piVar15[1] = iVar9;
            UNLOCK();
            if (iVar9 == 0) {
              (**(code **)(*piVar15 + 4))();
              LOCK();
              iVar9 = piVar15[2] + -1;
              piVar15[2] = iVar9;
              UNLOCK();
              if (iVar9 == 0) {
                iVar9 = *piVar15;
                goto LAB_00462abf;
              }
            }
          }
        }
        piStack_1b4 = (int *)*piStack_1b4;
        ppuVar22 = ppuVar16;
      } while (piStack_1b4 != (int *)*(int *)(param_1[5] + 0x1600c));
    }
    FUN_0059b7b0(ppuVar16[0xe],ppuVar16[0xf],(int)ppuVar16[0xf] - (int)ppuVar16[0xe] >> 3,
                 &LAB_0059a8e0);
    ppuStack_1a8 = (undefined **)0x4;
    piStack_1b4 = (int *)0x1c;
    piVar15 = (int *)(**(code **)(*(int *)*DAT_00e381e0 + 4))
                               (&piStack_1b4,&ppuStack_1a8,1,1,0,0xffffffff,0);
    if (piVar15 == (int *)0x0) {
      FUN_00b70479(&PTR_s_bad_allocation_00dc1bcc,1);
      ppuStack_1a8 = std::bad_alloc::vftable;
                    /* WARNING: Subroutine does not return */
      __CxxThrowException_8(&ppuStack_1a8,&DAT_00d42574);
    }
    pLVar18 = piVar15 + 1;
    *piVar15 = (int)NiRefObject::vftable;
    *pLVar18 = 0;
    InterlockedIncrement((LONG *)&DAT_00e381e8);
    piVar15[2] = 0;
    piVar15[3] = 0;
    piVar15[4] = 0;
    *(undefined2 *)(piVar15 + 5) = 0;
    *(undefined2 *)((int)piVar15 + 0x16) = 0;
    *piVar15 = (int)NiAlphaProperty::vftable;
    *(undefined2 *)(piVar15 + 6) = 0xec;
    *(undefined1 *)((int)piVar15 + 0x1a) = 0;
    InterlockedIncrement(pLVar18);
    *(undefined1 *)((int)piVar15 + 0x1a) = 0;
    *(ushort *)(piVar15 + 6) = *(ushort *)(piVar15 + 6) & 0xf2ed | 0x12ed;
    piStack_1bc = piVar15;
    InterlockedIncrement(pLVar18);
    FUN_00418a20(&piStack_1bc);
    LVar14 = InterlockedDecrement(pLVar18);
    if (LVar14 == 0) {
      (**(code **)(*piVar15 + 4))();
    }
    (**(code **)(*piStack_78 + 0x88))(uVar21,1);
    pfStack_16c = (float *)0x462bf6;
    LVar14 = InterlockedDecrement(pLVar18);
    if (LVar14 == 0) {
      (**(code **)(*piVar15 + 4))();
    }
    pfStack_16c = (float *)0x462c0a;
    LVar14 = InterlockedDecrement((LONG *)ppuStack_148);
    if (LVar14 == 0) {
      (**(code **)(*piStack_14c + 4))();
    }
    pfStack_16c = (float *)0x462c23;
    LVar14 = InterlockedDecrement(apLStack_e0[0]);
    if (LVar14 == 0) {
      (**(code **)(*piStack_130 + 4))();
    }
    pfStack_16c = (float *)*puStack_108;
    ppiStack_170 = &piStack_130;
    piStack_174 = (int *)0x462c48;
    FUN_0043e5b0();
  }
  if (puStack_108 != (undefined4 *)0x0) {
    pfStack_16c = (float *)0x462c75;
    (**(code **)(**(int **)(&DAT_00e1b748 + (puStack_108[-1] & 0xffff) * 4) + 0x10))();
  }
  return;
}

```

---

## `FUN_004a8b70` @ 004a8b70

- **signature**: `undefined FUN_004a8b70(void)`
- **triggered by strings**:
  - `s_LuaGetTerrainType_00cbb2b4`

```c

void FUN_004a8b70(void)

{
  int iVar1;
  int iVar2;
  undefined4 *puVar3;
  
  if (DAT_00e3d530 == 0) {
    iVar2 = FUN_0047d370(0x30);
    if (iVar2 == 0) {
      DAT_00e3d530 = 0;
    }
    else {
      DAT_00e3d530 = FUN_004318b0();
    }
  }
  FUN_00499ba0();
  FUN_004a8e80();
  FUN_005be830(DAT_00e1a17c);
  if (DAT_00e3d524 == 0) {
    iVar2 = FUN_0047d370(0xb4);
    if (iVar2 == 0) {
      DAT_00e3d524 = 0;
    }
    else {
      DAT_00e3d524 = FUN_0046ecb0();
    }
  }
  FUN_0046eeb0(DAT_00e3d524);
  FUN_004a8e30();
  iVar2 = DAT_00e3d534;
  FUN_00481570("WorldManager Init:");
  FUN_005e5e20(iVar2 + 0x24);
  iVar1 = DAT_00e3d540;
  *(undefined1 *)(iVar2 + 0x20) = 1;
  FUN_00994e1f(*(undefined4 *)(iVar1 + 0xc),FUN_005de460,"LuaGetTerrainType");
  FUN_005ce330();
  if (DAT_00e3d610 == 0) {
    iVar2 = FUN_0047d370(0xa0);
    if (iVar2 == 0) {
      DAT_00e3d610 = 0;
    }
    else {
      DAT_00e3d610 = FUN_004a8fe0();
    }
  }
  FUN_004c4ed0();
  FUN_008d8f1c(DAT_00e3d540,1);
  iVar2 = FUN_0047d370(0x380);
  if (iVar2 == 0) {
    iVar2 = 0;
  }
  else {
    iVar2 = FUN_004a8a30();
  }
  puVar3 = (undefined4 *)FUN_0047d370(4);
  if (puVar3 == (undefined4 *)0x0) {
    puVar3 = (undefined4 *)0x0;
  }
  else {
    *puVar3 = JobRequest::CompletionDeleter::vftable;
  }
  *(undefined4 **)(iVar2 + 0x374) = puVar3;
  *(undefined1 *)(iVar2 + 0x378) = 1;
  FUN_004a8860(iVar2);
  return;
}

```

---

## `FUN_00596880` @ 00596880

- **signature**: `undefined FUN_00596880(void)`
- **triggered by strings**:
  - `PTR_s_UOStaticTerrainShader_00dd5d50`

```c

undefined ** FUN_00596880(void)

{
  return &PTR_s_UOStaticTerrainShader_00dd5d50;
}

```

---

## `FUN_00596890` @ 00596890

- **signature**: `undefined FUN_00596890(void)`
- **triggered by strings**:
  - `s_UOStaticTerrainShader_00cb9610`

```c

undefined4 * FUN_00596890(undefined4 *param_1)

{
  int *piVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  int iVar5;
  LONG LVar6;
  int local_4;
  
  puVar3 = param_1;
  FUN_00751ca0();
  puVar3[0x38] = 0;
  *(undefined1 *)(puVar3 + 0x39) = 0;
  *puVar3 = UOStaticTerrainShader::vftable;
  puVar3[0x3a] = 0;
  puVar3[0x3b] = 0;
  puVar3[0x3c] = 0;
  puVar3[0x3d] = 0;
  *(undefined1 *)(puVar3 + 9) = 1;
  *(undefined1 *)((int)puVar3 + 0x25) = 0;
  iVar5 = FUN_00678b10("UOStaticTerrainShader");
  piVar1 = puVar3 + 2;
  local_4 = iVar5;
  if (*piVar1 != iVar5) {
    if (iVar5 != 0) {
      InterlockedIncrement((LONG *)(iVar5 + -8));
    }
    iVar2 = *piVar1;
    if (iVar2 != 0) {
      param_1 = (undefined4 *)(uint)*(ushort *)(iVar2 + -2);
      LVar6 = InterlockedDecrement((LONG *)(iVar2 + -8));
      if (LVar6 == 1) {
        FUN_00678e00(piVar1);
      }
    }
    *piVar1 = iVar5;
  }
  if (iVar5 != 0) {
    LVar6 = InterlockedDecrement((LONG *)(iVar5 + -8));
    if (LVar6 == 1) {
      FUN_00678e00(&local_4);
    }
  }
  FUN_007567c0(&param_1);
  if (*(short *)(puVar3 + 0x13) == 0) {
    FUN_00419650(puVar3 + 0x11,*(undefined2 *)((int)puVar3 + 0x52));
  }
  FUN_004197d0(&param_1);
  puVar3[0xf] = (uint)*(ushort *)(puVar3 + 0x14);
  iVar5 = FUN_006642d0();
  if (iVar5 == 0) {
    iVar5 = 0;
  }
  else {
    iVar5 = FUN_0074fad0();
  }
  puVar4 = param_1;
  puVar3[0x3a] = iVar5;
  iVar5 = *(int *)(iVar5 + 0xc);
  if (*(char *)(iVar5 + 0x15c) == '\0') {
    if (*(char *)(iVar5 + 0xac) != '\0') {
      *(undefined1 *)(iVar5 + 0xac) = 0;
      *(undefined1 *)(iVar5 + 0x15c) = 1;
      *(undefined4 *)(iVar5 + 300) = 1;
      *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
      *(int *)(iVar5 + 4) = *(int *)(iVar5 + 4) + -1;
    }
    *(undefined1 *)(iVar5 + 0x15c) = 1;
    *(undefined4 *)(iVar5 + 300) = 1;
    *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
  }
  else {
    *(undefined4 *)(iVar5 + 300) = 1;
  }
  FUN_00756db0(param_1[5]);
  iVar5 = FUN_006642d0();
  if (iVar5 == 0) {
    iVar5 = 0;
  }
  else {
    iVar5 = FUN_0074fad0();
  }
  puVar3[0x3b] = iVar5;
  iVar5 = *(int *)(iVar5 + 0xc);
  if (*(char *)(iVar5 + 0x15c) == '\0') {
    if (*(char *)(iVar5 + 0xac) != '\0') {
      *(undefined1 *)(iVar5 + 0xac) = 0;
      *(undefined1 *)(iVar5 + 0x15c) = 1;
      *(undefined4 *)(iVar5 + 300) = 1;
      *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
      *(int *)(iVar5 + 4) = *(int *)(iVar5 + 4) + -1;
    }
    *(undefined1 *)(iVar5 + 0x15c) = 1;
    *(undefined4 *)(iVar5 + 300) = 1;
    *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
  }
  else {
    *(undefined4 *)(iVar5 + 300) = 1;
  }
  FUN_00756db0(puVar4[5]);
  iVar5 = FUN_006642d0();
  if (iVar5 == 0) {
    iVar5 = 0;
  }
  else {
    iVar5 = FUN_0074fad0();
  }
  puVar3[0x3c] = iVar5;
  iVar5 = *(int *)(iVar5 + 0xc);
  if (*(char *)(iVar5 + 0x15c) == '\0') {
    if (*(char *)(iVar5 + 0xac) != '\0') {
      *(undefined1 *)(iVar5 + 0xac) = 0;
      *(undefined1 *)(iVar5 + 0x15c) = 1;
      *(undefined4 *)(iVar5 + 300) = 1;
      *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
      *(int *)(iVar5 + 4) = *(int *)(iVar5 + 4) + -1;
    }
    *(undefined1 *)(iVar5 + 0x15c) = 1;
    *(undefined4 *)(iVar5 + 300) = 1;
    *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
  }
  else {
    *(undefined4 *)(iVar5 + 300) = 1;
  }
  FUN_00756db0(puVar4[5]);
  iVar5 = FUN_006642d0();
  if (iVar5 == 0) {
    iVar5 = 0;
  }
  else {
    iVar5 = FUN_0074fad0();
  }
  puVar3[0x3d] = iVar5;
  iVar5 = *(int *)(iVar5 + 0xc);
  if (*(char *)(iVar5 + 0x15c) == '\0') {
    if (*(char *)(iVar5 + 0xac) != '\0') {
      *(undefined1 *)(iVar5 + 0xac) = 0;
      *(undefined1 *)(iVar5 + 0x15c) = 1;
      *(undefined4 *)(iVar5 + 300) = 1;
      *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
      *(int *)(iVar5 + 4) = *(int *)(iVar5 + 4) + -1;
    }
    *(undefined1 *)(iVar5 + 0x15c) = 1;
    *(undefined4 *)(iVar5 + 300) = 1;
    *(int *)(iVar5 + 0xb4) = *(int *)(iVar5 + 0xb4) + 1;
  }
  else {
    *(undefined4 *)(iVar5 + 300) = 1;
  }
  FUN_00756db0(puVar4[5]);
  piVar1 = puVar4 + 0x18;
  *piVar1 = *piVar1 + -1;
  if (*piVar1 == 0) {
    FUN_00756860();
  }
  return puVar3;
}

```

---

## `FUN_00597b90` @ 00597b90

- **signature**: `undefined FUN_00597b90(void)`
- **triggered by strings**:
  - `PTR_s_UOTerrainShader_00dd6098`

```c

undefined ** FUN_00597b90(void)

{
  return &PTR_s_UOTerrainShader_00dd6098;
}

```

---

## `FUN_00597c30` @ 00597c30

- **signature**: `undefined FUN_00597c30(void)`
- **triggered by strings**:
  - `s_UOTerrainShader_00ca5878`

```c

undefined4 * FUN_00597c30(undefined4 *param_1)

{
  int *piVar1;
  int iVar2;
  LONG LVar3;
  int iVar4;
  int iVar5;
  int local_1c;
  uint local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined **appuStack_c [3];
  
  FUN_00751ca0();
  param_1[0x38] = 0;
  *(undefined1 *)(param_1 + 0x39) = 0;
  *param_1 = UOTerrainShader::vftable;
  *(undefined1 *)(param_1 + 9) = 1;
  *(undefined1 *)((int)param_1 + 0x25) = 0;
  iVar2 = FUN_00678b10("UOTerrainShader");
  piVar1 = param_1 + 2;
  local_1c = iVar2;
  if (*piVar1 != iVar2) {
    if (iVar2 != 0) {
      InterlockedIncrement((LONG *)(iVar2 + -8));
    }
    iVar5 = *piVar1;
    if (iVar5 != 0) {
      local_18 = (uint)*(ushort *)(iVar5 + -2);
      LVar3 = InterlockedDecrement((LONG *)(iVar5 + -8));
      if (LVar3 == 1) {
        FUN_00678e00(piVar1);
      }
    }
    *piVar1 = iVar2;
  }
  if ((iVar2 != 0) && (LVar3 = InterlockedDecrement((LONG *)(iVar2 + -8)), LVar3 == 1)) {
    FUN_00678e00(&local_1c);
  }
  FUN_00419650(param_1 + 0x11,0x32);
  local_18 = 0;
  do {
    FUN_007567c0(&local_1c);
    if ((uint)*(ushort *)(param_1 + 0x13) <= (uint)*(ushort *)((int)param_1 + 0x4e)) {
      FUN_00419650(param_1 + 0x11,
                   (uint)*(ushort *)((int)param_1 + 0x52) + (uint)*(ushort *)((int)param_1 + 0x4e));
    }
    FUN_004197d0(&local_1c);
    iVar2 = local_1c;
    iVar5 = 0;
    do {
      local_14 = 4;
      local_10 = 0x60;
      iVar4 = (**(code **)(*(int *)*DAT_00e381e0 + 4))(&local_10,&local_14,1,1,0,0xffffffff,0);
      if (iVar4 == 0) {
        FUN_00b70479(&PTR_s_bad_allocation_00dc1bcc,1);
        appuStack_c[0] = std::bad_alloc::vftable;
                    /* WARNING: Subroutine does not return */
        __CxxThrowException_8(appuStack_c,&DAT_00d42574);
      }
      iVar4 = FUN_0074fad0();
      iVar4 = *(int *)(iVar4 + 0xc);
      if (*(char *)(iVar4 + 0x15c) == '\0') {
        if (*(char *)(iVar4 + 0xac) != '\0') {
          *(undefined1 *)(iVar4 + 0xac) = 0;
          *(undefined1 *)(iVar4 + 0x15c) = 1;
          *(undefined4 *)(iVar4 + 300) = 1;
          *(int *)(iVar4 + 0xb4) = *(int *)(iVar4 + 0xb4) + 1;
          *(int *)(iVar4 + 4) = *(int *)(iVar4 + 4) + -1;
        }
        *(undefined1 *)(iVar4 + 0x15c) = 1;
        *(undefined4 *)(iVar4 + 300) = 1;
        *(int *)(iVar4 + 0xb4) = *(int *)(iVar4 + 0xb4) + 1;
      }
      else {
        *(undefined4 *)(iVar4 + 300) = 1;
      }
      FUN_00750230();
      FUN_00756db0(*(undefined4 *)(iVar2 + 0x14));
      iVar5 = iVar5 + 1;
    } while (iVar5 < 8);
    piVar1 = (int *)(iVar2 + 0x60);
    *piVar1 = *piVar1 + -1;
    if (*piVar1 == 0) {
      FUN_00756860();
    }
    local_18 = local_18 + 1;
  } while ((int)local_18 < 0x32);
  return param_1;
}

```

---

## `FUN_00597e90` @ 00597e90

- **signature**: `undefined FUN_00597e90(void)`
- **triggered by strings**:
  - `PTR_s_UOTerrainTexturingProperty_00dd60a0`

```c

undefined4 __thiscall FUN_00597e90(int param_1)

{
  int *piVar1;
  undefined **ppuVar2;
  uint uVar3;
  int in_stack_00000010;
  
  piVar1 = *(int **)(in_stack_00000010 + 0x28);
  if ((piVar1 != (int *)0x0) &&
     (ppuVar2 = (undefined **)(**(code **)(*piVar1 + 8))(), ppuVar2 != (undefined **)0x0)) {
    while (ppuVar2 != &PTR_s_UOTerrainTexturingProperty_00dd60a0) {
      ppuVar2 = (undefined **)ppuVar2[1];
      if (ppuVar2 == (undefined **)0x0) {
        return 0;
      }
    }
    if (piVar1[0xe] == 0) {
      uVar3 = 0;
    }
    else {
      uVar3 = piVar1[0xf] - piVar1[0xe] >> 3;
    }
    *(uint *)(param_1 + 0x3c) = uVar3;
    if (0x31 < uVar3) {
      *(undefined4 *)(param_1 + 0x3c) = 0x31;
    }
  }
  return 0;
}

```

---

## `FUN_00597ef0` @ 00597ef0

- **signature**: `undefined FUN_00597ef0(void)`
- **triggered by strings**:
  - `PTR_s_UOTerrainTexturingProperty_00dd60a0`

```c

undefined4 __thiscall
FUN_00597ef0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,int param_5,
            undefined4 param_6,undefined4 param_7,undefined4 param_8)

{
  int *piVar1;
  int iVar2;
  int *piVar3;
  undefined **ppuVar4;
  
  piVar1 = *(int **)(param_5 + 0x28);
  if (piVar1 != (int *)0x0) {
    ppuVar4 = (undefined **)(**(code **)(*piVar1 + 8))();
    if (ppuVar4 != (undefined **)0x0) {
      while (ppuVar4 != &PTR_s_UOTerrainTexturingProperty_00dd60a0) {
        ppuVar4 = (undefined **)ppuVar4[1];
        if (ppuVar4 == (undefined **)0x0) {
          return 0;
        }
      }
      iVar2 = *(int *)(param_1 + 0x18);
      piVar3 = *(int **)(piVar1[0xe] + 4 + *(int *)(param_1 + 0x38) * 8);
      piVar1 = *(int **)(piVar1[0xe] + *(int *)(param_1 + 0x38) * 8);
      if (piVar3 != (int *)0x0) {
        LOCK();
        piVar3[1] = piVar3[1] + 1;
        UNLOCK();
      }
      (**(code **)(*piVar1 + 4))
                (*(undefined4 *)(param_1 + 0x40),*(undefined4 *)(param_1 + 0x38),param_2,param_3,
                 param_4,param_5,param_6,param_7,param_8,iVar2 + 0xa8);
      if (piVar3 != (int *)0x0) {
        LOCK();
        iVar2 = piVar3[1] + -1;
        piVar3[1] = iVar2;
        UNLOCK();
        if (iVar2 == 0) {
          (**(code **)(*piVar3 + 4))();
          LOCK();
          iVar2 = piVar3[2] + -1;
          piVar3[2] = iVar2;
          UNLOCK();
          if (iVar2 == 0) {
            (**(code **)(*piVar3 + 8))();
          }
        }
      }
    }
  }
  return 0;
}

```

---

## `FUN_009d4ad0` @ 009d4ad0

- **signature**: `undefined FUN_009d4ad0(void)`
- **triggered by strings**:
  - `PTR_s_AtlasTerrainShader_00de90b0`

```c

undefined ** FUN_009d4ad0(void)

{
  return &PTR_s_AtlasTerrainShader_00de90b0;
}

```

---

## `FUN_009d5ca0` @ 009d5ca0

- **signature**: `undefined FUN_009d5ca0(void)`
- **triggered by strings**:
  - `PTR_s_GameTerrainShader_00de90b8`

```c

undefined ** FUN_009d5ca0(void)

{
  return &PTR_s_GameTerrainShader_00de90b8;
}

```

---

## `FUN_009d6810` @ 009d6810

- **signature**: `undefined FUN_009d6810(void)`
- **triggered by strings**:
  - `s_GameTerrain_Offscreen.vsh_00d01084`
  - `s_GameTerrain_Offscreen.psh_00d010a0`
  - `s_GameTerrain_VertexLighting.vsh_00d010bc`
  - `s_GameTerrain_VertexLighting.psh_00d010dc`
  - `s_GameTerrain_HybridLighting.vsh_00d010fc`
  - `s_GameTerrain_HybridLighting.psh_00d0111c`

```c

undefined4 __fastcall FUN_009d6810(int *param_1)

{
  int *piVar1;
  int *piVar2;
  code *pcVar3;
  char cVar4;
  char cVar5;
  int *piVar6;
  undefined4 uVar7;
  int iVar8;
  int iVar9;
  bool bVar10;
  char *local_1b4;
  char *local_1b0;
  int *local_1a4 [50];
  undefined4 auStack_dc [52];
  void *local_c;
  undefined1 *puStack_8;
  int local_4;
  
  puStack_8 = &LAB_00c08026;
  local_c = ExceptionList;
  if ((char)param_1[4] != '\0') {
    return 1;
  }
  if (*(char *)((int)param_1 + 0x5e89) == '\0') {
    ExceptionList = &local_c;
    if (param_1[0x39] != 1) {
      if (param_1[0x39] == 2) {
        local_1b0 = "GameTerrain_VertexLighting.vsh";
        local_1b4 = "GameTerrain_VertexLighting.psh";
        ExceptionList = &local_c;
        goto LAB_009d6894;
      }
      ExceptionList = &local_c;
      param_1[0x39] = 1;
    }
    local_1b0 = "GameTerrain_HybridLighting.vsh";
    local_1b4 = "GameTerrain_HybridLighting.psh";
  }
  else {
    local_1b0 = "GameTerrain_Offscreen.vsh";
    local_1b4 = "GameTerrain_Offscreen.psh";
    ExceptionList = &local_c;
  }
LAB_009d6894:
  param_1[0x1844] = param_1[0x1844] + 1;
  piVar1 = param_1 + 0x183f;
  param_1[0x17a8] = param_1[0x17a8] + 1;
  piVar2 = param_1 + 0x17a3;
  local_4._0_1_ = 1;
  local_4._1_3_ = 0;
  bVar10 = DAT_00e381fc == (int *)0x0;
  param_1[0x45] = 0;
  *(undefined1 *)(param_1 + 0x42) = 0;
  local_1a4[0] = piVar2;
  local_1a4[1] = piVar1;
  if (bVar10) {
    *(undefined1 *)(param_1 + 4) = 0;
  }
  else {
    FUN_00751880();
    *(undefined1 *)(param_1 + 4) = 1;
  }
  cVar4 = FUN_00a686c0(local_1b4);
  cVar5 = FUN_00a68520(local_1b0);
  if (((bVar10) || (cVar4 == '\0')) || (cVar5 == '\0')) {
    *(undefined1 *)(param_1 + 4) = 0;
    local_4 = (uint)local_4._1_3_ << 8;
    piVar6 = param_1 + 0x17a8;
    *piVar6 = *piVar6 + -1;
    if (*piVar6 == 0) {
      FUN_009ae680(piVar2);
    }
    local_4 = 0xffffffff;
    param_1 = param_1 + 0x1844;
    *param_1 = *param_1 + -1;
    if (*param_1 == 0) {
      FUN_009ae680(piVar1);
    }
    uVar7 = 0;
  }
  else {
    if (*(char *)((int)param_1 + 0x5e89) == '\0') {
      FUN_009b8470(param_1 + 0x1993,piVar2,piVar1);
    }
    auStack_dc[2] = 0;
    local_1a4[2] = (int *)0x2;
    iVar8 = 1;
    if (*(char *)((int)param_1 + 0x5e89) == '\0') {
      auStack_dc[3] = 3;
      local_1a4[3] = (int *)0x2;
      iVar8 = 2;
    }
    pcVar3 = *(code **)(*DAT_00e381fc + 0xb0);
    auStack_dc[iVar8 + 2] = 5;
    local_1a4[iVar8 + 2] = (int *)0x1;
    iVar8 = iVar8 + 1;
    (*pcVar3)(iVar8,1);
    piVar6 = (int *)FUN_0058f2a0();
    iVar9 = 0;
    if (iVar8 != 0) {
      do {
        (**(code **)(*piVar6 + 0x48))(iVar9,auStack_dc[iVar9],local_1a4[iVar9],0);
        iVar9 = iVar9 + 1;
      } while (iVar9 < iVar8);
    }
    (**(code **)(*param_1 + 0x6c))(piVar6);
    local_4 = (uint)local_4._1_3_ << 8;
    piVar6 = param_1 + 0x17a8;
    *piVar6 = *piVar6 + -1;
    if (*piVar6 == 0) {
      FUN_009ae680(piVar2);
    }
    local_4 = 0xffffffff;
    param_1 = param_1 + 0x1844;
    *param_1 = *param_1 + -1;
    if (*param_1 == 0) {
      FUN_009ae680(piVar1);
    }
    uVar7 = 1;
  }
  ExceptionList = local_c;
  return uVar7;
}

```

---

## `FUN_009d7190` @ 009d7190

- **signature**: `undefined FUN_009d7190(void)`
- **triggered by strings**:
  - `PTR_s_GameTerrainTexturingProperty_00de90c0`

```c

undefined4 __thiscall
FUN_009d7190(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,int param_5,
            undefined4 param_6,float *param_7,undefined4 param_8)

{
  float fVar1;
  float fVar2;
  float *pfVar3;
  code *pcVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 *puVar7;
  char cVar8;
  undefined **ppuVar9;
  int iVar10;
  int iVar11;
  int *piVar12;
  uint uVar13;
  undefined4 *puVar14;
  undefined4 uVar15;
  int *piVar16;
  int iVar17;
  bool bVar18;
  float10 fVar19;
  float10 fVar20;
  float fVar21;
  char cStack_61;
  int iStack_60;
  int iStack_5c;
  int *local_58;
  int iStack_54;
  int iStack_50;
  float afStack_38 [4];
  float fStack_28;
  float fStack_24;
  float afStack_20 [7];
  
  local_58 = *(int **)(param_5 + 0x28);
  if (local_58 != (int *)0x0) {
    for (ppuVar9 = (undefined **)(**(code **)(*local_58 + 8))(); ppuVar9 != (undefined **)0x0;
        ppuVar9 = (undefined **)ppuVar9[1]) {
      if (ppuVar9 == &PTR_s_GameTerrainTexturingProperty_00de90c0) {
        local_58 = local_58 + 0xd;
        goto LAB_009d71eb;
      }
    }
  }
  if (param_1[0x17a0] == 0) {
    local_58 = (int *)0x0;
  }
  else {
    local_58 = (int *)(param_1[0x17a0] + 0x34);
  }
LAB_009d71eb:
  if (param_1[0x47] == 0) {
    cStack_61 = '\0';
    if (DAT_00e34c64 != '\0') {
      cStack_61 = DAT_00e38687;
    }
    iVar17 = param_1[0xe];
    iStack_5c = (**(code **)(*local_58 + 4))();
    afStack_38[0] = DAT_00ca1390;
    iStack_5c = iStack_5c + iVar17 * -6;
    if (iStack_5c < 7) {
      if (iStack_5c < 1) {
        param_1[0xf] = 0;
        return 0xffffffff;
      }
    }
    else {
      iStack_5c = 6;
    }
    param_1[0x17a1] = iStack_5c;
    afStack_38[1] = afStack_38[0];
    afStack_38[2] = afStack_38[0];
    afStack_38[3] = afStack_38[0];
    fStack_28 = afStack_38[0];
    fStack_24 = afStack_38[0];
    iVar10 = FUN_009b4170();
    piVar12 = (int *)param_1[0x1855];
    *(undefined1 *)(piVar12 + 3) = 0;
    piVar12[1] = 0;
    piVar12[2] = 2;
    if (*piVar12 != iVar10) {
      *piVar12 = iVar10;
    }
    iVar10 = FUN_009b4170();
    piVar12 = (int *)param_1[0x185d];
    *(undefined1 *)(piVar12 + 3) = 0;
    piVar12[1] = 0;
    piVar12[2] = 2;
    if (*piVar12 != iVar10) {
      *piVar12 = iVar10;
    }
    uVar15 = DAT_00d0a4c4;
    iVar10 = *local_58;
    iStack_54 = -1;
    iStack_50 = -1;
    puVar14 = (undefined4 *)param_1[0x17f9];
    *puVar14 = DAT_00d0a4c4;
    puVar14[1] = uVar15;
    puVar14[2] = uVar15;
    puVar14[3] = uVar15;
    iVar10 = (**(code **)(iVar10 + 0xc))();
    iVar11 = (**(code **)(*local_58 + 0x10))();
    pfVar3 = (float *)param_1[0x17f1];
    *pfVar3 = (float)iVar10;
    pfVar3[1] = (float)iVar11;
    pfVar3[2] = (float)iVar10;
    pfVar3[3] = (float)iVar11;
    *(int *)param_1[0x1831] = iStack_5c;
    piVar12 = param_1 + 0x1895;
    iVar10 = 6;
    do {
      puVar14 = (undefined4 *)*piVar12;
      piVar12 = piVar12 + 8;
      iVar10 = iVar10 + -1;
      *puVar14 = 0;
    } while (iVar10 != 0);
    iStack_60 = 0;
    if (0 < iStack_5c) {
      do {
        piVar12 = (int *)(**(code **)(*local_58 + 8))(iVar17 * 6 + iStack_60);
        if (piVar12 == (int *)0x0) {
          iVar10 = FUN_009b4080();
          piVar12 = (int *)param_1[iStack_60 * 8 + 0x1865];
          *(undefined1 *)(piVar12 + 3) = 0;
          piVar12[1] = 3;
          piVar12[2] = 0;
          if (*piVar12 != iVar10) {
            *piVar12 = iVar10;
          }
          *(undefined4 *)param_1[iStack_60 * 8 + 0x1895] = 1;
          afStack_20[iStack_60] = 0.0;
        }
        else {
          iVar10 = (**(code **)(*piVar12 + 0x10))();
          if (iVar10 != 0) {
            if (iStack_60 == 0) {
              if ((1 < iStack_5c) || (param_1[0xe] != 0)) {
                iVar10 = (**(code **)(*piVar12 + 0x10))();
                piVar16 = (int *)param_1[0x1855];
LAB_009d73da:
                piVar16[2] = 2;
                piVar16[1] = 0;
                *(undefined1 *)(piVar16 + 3) = 0;
                if (*piVar16 != iVar10) {
                  *piVar16 = iVar10;
                }
              }
            }
            else if (iStack_60 == 3) {
              iVar10 = (**(code **)(*piVar12 + 0x10))();
              piVar16 = (int *)param_1[0x185d];
              goto LAB_009d73da;
            }
          }
          cVar8 = (**(code **)(*piVar12 + 0x28))();
          uVar13 = -(uint)(cVar8 != '\0') & 3;
          iVar10 = (**(code **)(*piVar12 + 8))();
          if (iVar10 == 0) {
            iVar10 = FUN_009b4080();
          }
          piVar16 = (int *)param_1[iStack_60 * 8 + 0x1865];
          *(undefined1 *)(piVar16 + 3) = 0;
          piVar16[1] = uVar13;
          piVar16[2] = 2;
          if (*piVar16 != iVar10) {
            *piVar16 = iVar10;
          }
          iVar10 = (**(code **)(*piVar12 + 0x3c))();
          if ((iVar10 < 0) || (2 < iVar10)) {
            iVar10 = 0;
          }
          *(int *)param_1[iStack_60 * 8 + 0x1895] = iVar10 + 1;
          iVar10 = (**(code **)(*piVar12 + 0x40))();
          pcVar4 = *(code **)(*piVar12 + 0x34);
          afStack_38[iStack_60] = DAT_00d0a0a8 / (float)iVar10;
          cVar8 = (*pcVar4)();
          if (cVar8 == '\0') {
            puVar14 = (undefined4 *)param_1[iStack_60 * 8 + 0x18f5];
            afStack_20[iStack_60] = 0.0;
            *puVar14 = 0;
LAB_009d7564:
            piVar12 = (int *)param_1[iStack_60 * 8 + 0x18c5];
            *(undefined1 *)(piVar12 + 3) = 1;
            if (*piVar12 != 0) {
              *piVar12 = 0;
            }
          }
          else {
            if (iStack_54 < 0) {
              iStack_54 = iStack_60;
            }
            iStack_50 = iStack_60;
            puVar14 = (undefined4 *)(**(code **)(*piVar12 + 0x30))();
            uVar15 = puVar14[1];
            uVar5 = *puVar14;
            uVar6 = puVar14[2];
            fVar19 = (float10)(**(code **)(*piVar12 + 0x38))();
            puVar14 = (undefined4 *)param_1[iStack_60 * 8 + 0x1925];
            iVar10 = *piVar12;
            afStack_20[iStack_60] = (float)fVar19;
            *puVar14 = uVar5;
            puVar14[3] = (float)fVar19;
            puVar14[1] = uVar15;
            puVar14[2] = uVar6;
            iVar10 = (**(code **)(iVar10 + 0xc))();
            if (iVar10 == 0) {
              *(undefined4 *)param_1[iStack_60 * 8 + 0x18f5] = 0;
              goto LAB_009d7564;
            }
            *(undefined4 *)param_1[iStack_60 * 8 + 0x18f5] = 1;
            piVar12 = (int *)param_1[iStack_60 * 8 + 0x18c5];
            *(undefined1 *)(piVar12 + 3) = 0;
            piVar12[1] = uVar13;
            piVar12[2] = 2;
            if (*piVar12 != iVar10) {
              *piVar12 = iVar10;
            }
          }
          FUN_009d6d00(param_1,param_2);
        }
        iStack_60 = iStack_60 + 1;
      } while (iStack_60 < iStack_5c);
    }
    if ((cStack_61 == '\0') || (iStack_54 < 0)) {
      *(undefined4 *)param_1[0x1809] = 0;
      *(undefined4 *)param_1[0x196d] = 0;
      uVar15 = DAT_00d0a4c0;
      iVar17 = 0;
      if (0 < iStack_5c) {
        piVar12 = param_1 + 0x1925;
        do {
          if (afStack_20[iVar17] == 0.0) {
            puVar14 = (undefined4 *)*piVar12;
            *puVar14 = 0;
            puVar14[1] = 0;
            puVar14[2] = 0;
            puVar14[3] = uVar15;
          }
          iVar17 = iVar17 + 1;
          piVar12 = piVar12 + 8;
        } while (iVar17 < iStack_5c);
      }
    }
    else {
      *(undefined4 *)param_1[0x1809] = 1;
      iVar17 = 0;
      *(undefined4 *)param_1[0x196d] = 1;
      if (0 < iStack_54) {
        piVar12 = param_1 + 0x1925;
        do {
          puVar14 = (undefined4 *)*piVar12;
          fVar1 = afStack_20[iStack_54];
          afStack_20[iVar17] = fVar1;
          iVar17 = iVar17 + 1;
          piVar12 = piVar12 + 8;
          *puVar14 = 0;
          puVar14[1] = 0;
          puVar14[2] = 0;
          puVar14[3] = fVar1;
        } while (iVar17 < iStack_54);
      }
      iVar17 = iStack_54 + 1;
      fVar19 = (float10)0.0;
      local_58 = (int *)0x0;
      if (iVar17 <= iStack_50) {
        iVar10 = iStack_54 << 5;
        do {
          fVar1 = afStack_20[iVar17];
          if (0.0 < fVar1) {
            local_58 = (int *)((int)local_58 + 1);
            iVar11 = iStack_54 + 1;
            fVar19 = (float10)0.6931471805599453 * (float10)fVar1 + fVar19;
            if (iVar11 < iVar17) {
              fVar2 = afStack_20[iStack_54];
              puVar14 = (undefined4 *)(iVar10 + 0x64b4 + (int)param_1);
              iVar10 = iVar11 - iStack_54;
              iVar11 = iVar17 - iVar11;
              do {
                puVar7 = (undefined4 *)*puVar14;
                fVar21 = (float)iVar10;
                puVar14 = puVar14 + 8;
                iVar10 = iVar10 + 1;
                iVar11 = iVar11 + -1;
                *puVar7 = 0;
                puVar7[1] = 0;
                puVar7[2] = 0;
                puVar7[3] = (fVar21 / (float)(iVar17 - iStack_54)) * (fVar1 - fVar2) + fVar2;
              } while (iVar11 != 0);
            }
            iVar10 = iVar17 << 5;
            iStack_54 = iVar17;
          }
          iVar17 = iVar17 + 1;
        } while (iVar17 <= iStack_50);
      }
      pfVar3 = (float *)param_1[0x1801];
      iVar17 = iStack_50 + 1;
      fVar20 = (float10)1.4426950408889634 * (fVar19 / (float10)(int)local_58);
      fVar19 = ROUND(fVar20);
      fVar20 = (float10)f2xm1(fVar20 - fVar19);
      fVar19 = (float10)fscale((float10)1 + fVar20,fVar19);
      *pfVar3 = (float)fVar19;
      pfVar3[1] = (float)fVar19;
      pfVar3[2] = (float)fVar19;
      pfVar3[3] = (float)fVar19;
      if (iVar17 < iStack_5c) {
        piVar12 = param_1 + iVar17 * 8 + 0x1925;
        do {
          puVar14 = (undefined4 *)*piVar12;
          fVar1 = afStack_20[iStack_50];
          afStack_20[iVar17] = fVar1;
          iVar17 = iVar17 + 1;
          piVar12 = piVar12 + 8;
          *puVar14 = 0;
          puVar14[1] = 0;
          puVar14[2] = 0;
          puVar14[3] = fVar1;
        } while (iVar17 < iStack_5c);
      }
    }
    pfVar3 = (float *)param_1[0x1955];
    *pfVar3 = afStack_38[0];
    pfVar3[1] = afStack_38[1];
    pfVar3[2] = afStack_38[2];
    fVar1 = DAT_00c9d1a0;
    pfVar3[3] = DAT_00c9d1a0;
    pfVar3 = (float *)param_1[0x195d];
    *pfVar3 = afStack_38[3];
    pfVar3[1] = fStack_28;
    pfVar3[2] = fStack_24;
    pfVar3[3] = fVar1;
    if (param_1[0xe] == 0) {
      *(undefined4 *)param_1[0x184d] = 1;
      if (*(char *)((int)param_1 + 0x5e89) == '\0') {
        (**(code **)(*param_1 + 0xa4))(param_1 + 0x1993,param_6,param_8,0,0,0,&DAT_00de437c,0,1,0);
      }
      else {
        iVar17 = *(int *)(param_1[0x17a0] + 0x38);
        iVar10 = param_1[7];
        *(undefined4 *)param_1[0x198d] = *(undefined4 *)(iVar17 + 0x14);
        uVar13 = (uint)*(byte *)(iVar17 + 0x18);
        if (*(uint *)(iVar10 + 0x730) != uVar13) {
          (**(code **)(**(int **)(iVar10 + 0x2238) + 0xe4))(*(int **)(iVar10 + 0x2238),0xc2,uVar13);
          *(uint *)(iVar10 + 0x730) = uVar13;
        }
      }
      iVar17 = param_1[7];
      if (*(int *)(iVar17 + 0x1f8) != 0) {
        (**(code **)(**(int **)(iVar17 + 0x2238) + 0xe4))(*(int **)(iVar17 + 0x2238),0x1b,0);
        *(undefined4 *)(iVar17 + 0x1f8) = 0;
      }
    }
    else {
      *(undefined4 *)param_1[0x184d] = 0;
      if (*(char *)((int)param_1 + 0x5e89) == '\0') {
        (**(code **)(*param_1 + 0xa8))(param_1 + 0x1993,10);
      }
      iVar17 = param_1[7];
      if (*(int *)(iVar17 + 0x1f8) != 1) {
        (**(code **)(**(int **)(iVar17 + 0x2238) + 0xe4))(*(int **)(iVar17 + 0x2238),0x1b,1);
        *(undefined4 *)(iVar17 + 0x1f8) = 1;
      }
      iVar17 = param_1[7];
      if (*(int *)(iVar17 + 0x1c0) != 5) {
        (**(code **)(**(int **)(iVar17 + 0x2238) + 0xe4))(*(int **)(iVar17 + 0x2238),0x14,5);
        *(undefined4 *)(iVar17 + 0x1c0) = 5;
      }
      iVar17 = param_1[7];
      if (*(int *)(iVar17 + 0x1b8) != 2) {
        (**(code **)(**(int **)(iVar17 + 0x2238) + 0xe4))(*(int **)(iVar17 + 0x2238),0x13,2);
        *(undefined4 *)(iVar17 + 0x1b8) = 2;
      }
    }
    bVar18 = *(char *)((int)param_1 + 0x5e89) == '\0';
    if (!bVar18) goto LAB_009d7aca;
    if (param_1[0xe] == param_1[0xf] + -1) {
      (**(code **)(*param_1 + 0xb0))(param_5,param_6);
      uVar13 = (uint)*(byte *)(param_1 + 0x3a);
      iVar17 = param_1[7];
      if (*(uint *)(iVar17 + 0x200) != uVar13) {
        (**(code **)(**(int **)(iVar17 + 0x2238) + 0xe4))(*(int **)(iVar17 + 0x2238),0x1c,uVar13);
        *(uint *)(iVar17 + 0x200) = uVar13;
      }
      iVar17 = param_1[0x41];
      iVar10 = param_1[7];
      if (*(int *)(iVar10 + 0x230) != iVar17) {
        (**(code **)(**(int **)(iVar10 + 0x2238) + 0xe4))(*(int **)(iVar10 + 0x2238),0x22,iVar17);
        *(int *)(iVar10 + 0x230) = iVar17;
      }
      FUN_009baf40();
    }
    else {
      iVar17 = param_1[7];
      if (*(int *)(iVar17 + 0x200) != 0) {
        (**(code **)(**(int **)(iVar17 + 0x2238) + 0xe4))(*(int **)(iVar17 + 0x2238),0x1c,0);
        *(undefined4 *)(iVar17 + 0x200) = 0;
      }
      fVar1 = DAT_00c9d1a0;
      pfVar3 = (float *)param_1[0x17e9];
      *pfVar3 = DAT_00c9d1a0;
      pfVar3[1] = 0.0;
      pfVar3[2] = fVar1;
      pfVar3[3] = 0.0;
    }
  }
  bVar18 = *(char *)((int)param_1 + 0x5e89) == '\0';
LAB_009d7aca:
  if (bVar18) {
    *(undefined4 *)param_1[0x1975] = 0;
    *(undefined4 *)param_1[0x1829] = 0;
    fVar1 = param_7[0xc];
    pfVar3 = (float *)param_1[0x1821];
    *pfVar3 = fVar1 * *param_7;
    pfVar3[1] = param_7[1] * fVar1;
    pfVar3[2] = param_7[2] * fVar1;
    pfVar3[3] = param_7[9];
    iVar17 = param_1[0x1822];
    if (1 < iVar17) {
      pfVar3[4] = param_7[3] * fVar1;
      pfVar3[5] = param_7[4] * fVar1;
      pfVar3[6] = param_7[5] * fVar1;
      pfVar3[7] = param_7[10];
      if (2 < iVar17) {
        pfVar3[8] = param_7[6] * fVar1;
        pfVar3[9] = param_7[7] * fVar1;
        pfVar3[10] = param_7[8] * fVar1;
        pfVar3[0xb] = param_7[0xb];
        if (3 < iVar17) {
          pfVar3[0xc] = 0.0;
          pfVar3[0xd] = 0.0;
          pfVar3[0xe] = 0.0;
          pfVar3[0xf] = DAT_00c9d1a0;
        }
      }
    }
  }
  if (*(char *)((int)param_1 + 0x5e89) != '\0') {
    return 0;
  }
  uVar15 = FUN_009b8d70(param_2,param_3,param_4,param_5,param_6,param_7,param_8);
  return uVar15;
}

```

---

## `FUN_00a68250` @ 00a68250

- **signature**: `undefined FUN_00a68250(void)`
- **triggered by strings**:
  - `s_AtlasTerrain.vsh_00d00f6c`

```c

undefined1 __fastcall FUN_00a68250(int param_1)

{
  int *piVar1;
  undefined1 uVar2;
  void *local_c;
  undefined1 *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_00c07e98;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
  local_4 = 0;
  uVar2 = FUN_009aef60("AtlasTerrain.vsh");
  FUN_009b1ac0(2);
  FUN_009b1ac0(2);
  FUN_009b1ac0(2);
  FUN_009b1ac0(2);
  FUN_009b1ac0(2);
  FUN_009b1ac0(2);
  FUN_009b1600();
  FUN_009b1ac0(2);
  FUN_009b1ac0(4);
  FUN_009b1ac0(3);
  local_4 = 0xffffffff;
  piVar1 = (int *)(param_1 + 0x14);
  *piVar1 = *piVar1 + -1;
  if (*piVar1 == 0) {
    FUN_009ae680(param_1);
  }
  ExceptionList = local_c;
  return uVar2;
}

```

---

## `FUN_00a68360` @ 00a68360

- **signature**: `undefined FUN_00a68360(void)`
- **triggered by strings**:
  - `s_AtlasTerrain.psh_00d00f80`

```c

undefined1 __fastcall FUN_00a68360(int param_1)

{
  int *piVar1;
  undefined1 uVar2;
  void *local_c;
  undefined1 *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_00c07e78;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  *(int *)(param_1 + 0x14) = *(int *)(param_1 + 0x14) + 1;
  local_4 = 0;
  uVar2 = FUN_009af090("AtlasTerrain.psh");
  FUN_009b1600();
  FUN_009b1600();
  FUN_009b1600();
  FUN_009b1600();
  FUN_009b1600();
  FUN_009b1600();
  FUN_009b1600();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1b90();
  FUN_009b1ac0(2);
  FUN_009b1b90();
  FUN_009b1600();
  local_4 = 0xffffffff;
  piVar1 = (int *)(param_1 + 0x14);
  *piVar1 = *piVar1 + -1;
  if (*piVar1 == 0) {
    FUN_009ae680(param_1);
  }
  ExceptionList = local_c;
  return uVar2;
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

## `FUN_00c12a60` @ 00c12a60

- **signature**: `undefined FUN_00c12a60(void)`
- **triggered by strings**:
  - `s_UOTerrainShader_00ca5878`
  - `s_UOStaticTerrainShader_00cb9610`

```c

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00c12a60(void)

{
  char *pcVar1;
  
  _DAT_00e3a1a4 =
       type_info::name((type_info *)&UOTerrainShader::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a1a4 = _DAT_00e3a1a4 + 6;
  DAT_00e3a1a0 = "UOTerrainShader";
  DAT_00e3a1a8 = &LAB_00591ad0;
  DAT_00e3a1ac = FUN_00592c70;
  DAT_00e3a1b0 = 0xffff0000;
  DAT_00e3a1b4 = 0xfffe0000;
  DAT_00e3a1b8 = 0;
  pcVar1 = type_info::name((type_info *)&UOWaterShader::RTTI_Type_Descriptor,
                           (__type_info_node *)&DAT_00e0b6fc);
  DAT_00e3a1c0 = pcVar1 + 6;
  DAT_00e3a1bc = "UOWaterShader";
  _DAT_00e3a1c4 = &LAB_0059e240;
  _DAT_00e3a1c8 = FUN_00592c90;
  _DAT_00e3a1cc = 0xffff0000;
  _DAT_00e3a1d0 = 0xfffe0000;
  DAT_00e3a1d4 = 0;
  _DAT_00e3a1dc =
       type_info::name((type_info *)&UOSpriteShaderHLSL::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a1dc = _DAT_00e3a1dc + 6;
  _DAT_00e3a1d8 = "UOSpriteShader";
  _DAT_00e3a1e0 = &LAB_005954d0;
  _DAT_00e3a1e4 = FUN_00592cb0;
  _DAT_00e3a1e8 = 0xffff0200;
  _DAT_00e3a1ec = 0xfffe0101;
  _DAT_00e3a1f0 = 0;
  _DAT_00e3a1f8 =
       type_info::name((type_info *)&UOSpriteShaderFFP::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a1f8 = _DAT_00e3a1f8 + 6;
  _DAT_00e3a1f4 = "UOSpriteShader";
  _DAT_00e3a1fc = &LAB_00594090;
  _DAT_00e3a200 = FUN_00592cd0;
  _DAT_00e3a204 = 0xffff0000;
  _DAT_00e3a208 = 0xfffe0000;
  _DAT_00e3a20c = 0;
  _DAT_00e3a214 =
       type_info::name((type_info *)&UOSpriteShaderMob::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a214 = _DAT_00e3a214 + 6;
  _DAT_00e3a210 = "UOSpriteShaderMob";
  _DAT_00e3a218 = &LAB_00594190;
  _DAT_00e3a21c = FUN_00592cf0;
  _DAT_00e3a220 = 0xffff0000;
  _DAT_00e3a224 = 0xfffe0000;
  _DAT_00e3a228 = 0;
  _DAT_00e3a230 =
       type_info::name((type_info *)&UOSpriteShaderShadow::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a230 = _DAT_00e3a230 + 6;
  _DAT_00e3a22c = "UOSpriteShaderShadow";
  _DAT_00e3a234 = &LAB_00594ba0;
  _DAT_00e3a238 = FUN_00592d10;
  _DAT_00e3a23c = 0xffff0000;
  _DAT_00e3a240 = 0xfffe0000;
  _DAT_00e3a244 = 0;
  _DAT_00e3a24c =
       type_info::name((type_info *)&UOSpriteUIShaderHLSL::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a24c = _DAT_00e3a24c + 6;
  _DAT_00e3a248 = "UOSpriteUIShader";
  _DAT_00e3a250 = &LAB_00596870;
  _DAT_00e3a254 = FUN_00592d30;
  _DAT_00e3a258 = 0xffff0200;
  _DAT_00e3a25c = 0xfffe0101;
  _DAT_00e3a260 = 0;
  _DAT_00e3a268 =
       type_info::name((type_info *)&UOSpriteUIShaderFFP::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a268 = _DAT_00e3a268 + 6;
  _DAT_00e3a264 = "UOSpriteUIShader";
  _DAT_00e3a26c = &LAB_005959c0;
  _DAT_00e3a270 = FUN_00592d50;
  _DAT_00e3a274 = 0xffff0000;
  _DAT_00e3a278 = 0xfffe0000;
  _DAT_00e3a27c = 0;
  _DAT_00e3a284 =
       type_info::name((type_info *)&UOLightingShader::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a284 = _DAT_00e3a284 + 6;
  _DAT_00e3a280 = "UOLightingShader";
  _DAT_00e3a288 = &LAB_00590fd0;
  _DAT_00e3a28c = FUN_00592d70;
  _DAT_00e3a290 = 0xffff0000;
  _DAT_00e3a294 = 0xfffe0000;
  _DAT_00e3a298 = 0;
  _DAT_00e3a2a0 =
       type_info::name((type_info *)&UOStaticTerrainShader::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a2a0 = _DAT_00e3a2a0 + 6;
  _DAT_00e3a29c = "UOStaticTerrainShader";
  _DAT_00e3a2a4 = &LAB_00597b30;
  _DAT_00e3a2a8 = FUN_00592d90;
  _DAT_00e3a2ac = 0xffff0000;
  _DAT_00e3a2b0 = 0xfffe0000;
  _DAT_00e3a2b4 = 0;
  _DAT_00e3a2bc =
       type_info::name((type_info *)&UOShadowShader::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a2bc = _DAT_00e3a2bc + 6;
  _DAT_00e3a2b8 = "UOShadowShader";
  _DAT_00e3a2c0 = &LAB_005936f0;
  _DAT_00e3a2c4 = FUN_00592db0;
  _DAT_00e3a2c8 = 0xffff0000;
  _DAT_00e3a2cc = 0xfffe0000;
  _DAT_00e3a2d0 = 0;
  _DAT_00e3a2d8 =
       type_info::name((type_info *)&UOSpriteShaderDepthOnly::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a2d8 = _DAT_00e3a2d8 + 6;
  _DAT_00e3a2d4 = "UOSpriteShaderDepthOnly";
  _DAT_00e3a2dc = &LAB_00594690;
  _DAT_00e3a2e0 = FUN_00592dd0;
  _DAT_00e3a2e4 = 0xffff0000;
  _DAT_00e3a2e8 = 0xfffe0000;
  _DAT_00e3a2ec = 0;
  _DAT_00e3a2f4 =
       type_info::name((type_info *)&UONightMapShader::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a2f4 = _DAT_00e3a2f4 + 6;
  _DAT_00e3a2f0 = "UONightMapShader";
  _DAT_00e3a2f8 = &LAB_00591610;
  _DAT_00e3a2fc = FUN_00592df0;
  _DAT_00e3a300 = 0xffff0000;
  _DAT_00e3a304 = 0xfffe0000;
  _DAT_00e3a308 = 0;
  _DAT_00e3a310 =
       type_info::name((type_info *)&UODeathShaderHLSL::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a310 = _DAT_00e3a310 + 6;
  _DAT_00e3a30c = "UODeathShader";
  _DAT_00e3a314 = &LAB_004189e0;
  _DAT_00e3a318 = FUN_00592e10;
  _DAT_00e3a31c = 0xffff0200;
  _DAT_00e3a320 = 0xfffe0101;
  _DAT_00e3a324 = 0;
  _DAT_00e3a32c =
       type_info::name((type_info *)&UODeathShaderFFP::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a32c = _DAT_00e3a32c + 6;
  _DAT_00e3a328 = "UODeathShader";
  _DAT_00e3a330 = &LAB_004182f0;
  _DAT_00e3a334 = FUN_00592e30;
  _DAT_00e3a338 = 0xffff0000;
  _DAT_00e3a33c = 0xfffe0000;
  _DAT_00e3a340 = 0;
  _DAT_00e3a348 =
       type_info::name((type_info *)&UOFadeShader::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a348 = _DAT_00e3a348 + 6;
  _DAT_00e3a344 = "UOFadeShader";
  _DAT_00e3a34c = &LAB_004263f0;
  _DAT_00e3a350 = FUN_00592e50;
  _DAT_00e3a354 = 0xffff0000;
  _DAT_00e3a358 = 0xfffe0000;
  _DAT_00e3a35c = 0;
  _DAT_00e3a364 =
       type_info::name((type_info *)&UOEffectsShaderHLSL::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a364 = _DAT_00e3a364 + 6;
  _DAT_00e3a360 = "UOEffectsShader";
  _DAT_00e3a368 = &LAB_005904b0;
  _DAT_00e3a36c = FUN_00592e70;
  _DAT_00e3a370 = 0xffff0200;
  _DAT_00e3a374 = 0xfffe0101;
  DAT_00e3a378 = 0;
  _DAT_00e3a380 =
       type_info::name((type_info *)&UOEffectsShaderFFP::RTTI_Type_Descriptor,
                       (__type_info_node *)&DAT_00e0b6fc);
  _DAT_00e3a380 = _DAT_00e3a380 + 6;
  _DAT_00e3a37c = "UOEffectsShader";
  _DAT_00e3a384 = &LAB_0058fc60;
  _DAT_00e3a388 = FUN_00592e90;
  _DAT_00e3a38c = 0xffff0000;
  _DAT_00e3a390 = 0xfffe0000;
  DAT_00e3a394 = 0;
  _atexit((_func_4879 *)&LAB_00c163a0);
  return;
}

```

---

