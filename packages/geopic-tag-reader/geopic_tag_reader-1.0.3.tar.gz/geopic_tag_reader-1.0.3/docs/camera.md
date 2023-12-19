<!-- markdownlint-disable -->

<a href="../geopic_tag_reader/camera.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `camera`




**Global Variables**
---------------
- **EQUIRECTANGULAR_MODELS**

---

<a href="../geopic_tag_reader/camera.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_360`

```python
is_360(make: Optional[str], model: Optional[str]) → bool
```

Checks if given camera is equirectangular (360°) based on its make and model. 

``` is_360(None, None)```
False
``` is_360("GoPro", None)``` False ``` is_360("GoPro", "Max 360")```
True





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
