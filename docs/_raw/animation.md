# animation

Auto-generated from `tools/ghidra/ghidra_dump.json`.

Functions discovered via xrefs from strings matching: `MobAnim, AnimationFrame, AnimationLegacyFrameSet`

Total: 4 unique decompiled functions.

---

## `FUN_00431050` @ 00431050

- **signature**: `undefined FUN_00431050(void)`
- **triggered by strings**:
  - `PTR_s_MobAnimTriShape_00dc52f0`

```c

undefined ** FUN_00431050(void)

{
  return &PTR_s_MobAnimTriShape_00dc52f0;
}

```

---

## `FUN_00431130` @ 00431130

- **signature**: `undefined FUN_00431130(void)`
- **triggered by strings**:
  - `PTR_s_MobAnimTriShapeShadow_00dc5300`

```c

undefined ** FUN_00431130(void)

{
  return &PTR_s_MobAnimTriShapeShadow_00dc5300;
}

```

---

## `FUN_00431220` @ 00431220

- **signature**: `undefined FUN_00431220(void)`
- **triggered by strings**:
  - `PTR_s_MobAnimTexture_00dc52f8`

```c

undefined ** FUN_00431220(void)

{
  return &PTR_s_MobAnimTexture_00dc52f8;
}

```

---

## `FUN_00a71a4d` @ 00a71a4d

- **signature**: `undefined FUN_00a71a4d(void)`
- **triggered by strings**:
  - `s_AnimationFrame_00ca1d9c`

```c

void FUN_00a71a4d(void)

{
  char cVar1;
  char *_Dest;
  undefined4 ***pppuVar2;
  uint uVar3;
  undefined4 **local_30 [5];
  uint local_1c;
  void *local_14;
  undefined1 *puStack_10;
  undefined4 local_c;
  
  local_c = 0xffffffff;
  puStack_10 = &LAB_00c037c0;
  local_14 = ExceptionList;
  uVar3 = 0;
  ExceptionList = &local_14;
  do {
    local_1c = 0xf;
    FUN_00405fd0(0);
    local_c = 0;
    FUN_00427b70("AnimationFrame");
    if (uVar3 != 0) {
      _Dest = (char *)FUN_0047d3e0(2);
      _sprintf(_Dest,"%d",uVar3);
      FUN_0047f1b0(_Dest);
      FUN_0047d560(_Dest);
    }
    FUN_0047f1b0(&DAT_00d02e44);
    pppuVar2 = (undefined4 ***)local_30[0];
    if (local_1c < 0x10) {
      pppuVar2 = local_30;
    }
    cVar1 = FUN_0098e42d(pppuVar2,1);
    if (cVar1 != '\0') {
      pppuVar2 = (undefined4 ***)local_30[0];
      if (local_1c < 0x10) {
        pppuVar2 = local_30;
      }
      FUN_0098e793(pppuVar2);
    }
    local_c = 0xffffffff;
    FUN_00403770();
    uVar3 = uVar3 + 1;
  } while (uVar3 < 10);
  ExceptionList = local_14;
  return;
}

```

---

