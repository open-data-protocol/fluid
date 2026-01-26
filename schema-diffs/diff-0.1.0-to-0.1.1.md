# Schema Changes: 0.1.0 → 0.1.1

**Total changes:** 4
- ✅ Added: 0
- ❌ Removed: 0
- 📝 Modified: 4

---

## 📝 Modified Properties

### `$defs.accessGrant.required`

**Before:**
```json
["principal", "permissions"]
```

**After:**
```json
[]
```

### `$defs.notification.required`

**Before:**
```json
["channel", "target"]
```

**After:**
```json
[]
```

### `$defs.runtime.required`

**Before:**
```json
["platform"]
```

**After:**
```json
[]
```

### `properties.fluidVersion.examples`

**Before:**
```json
["0.1.0"]
```

**After:**
```json
["0.1.1"]
```
