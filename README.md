# 现代C++通讲

## 编译方法

```console
$ scons
```

然后可以在 `build/debug/src/` 目录下找到 `cpp_lessons.notes.pdf` 和 `cpp_lessons.no_notes.pdf` 两个文件。
其中第一个携带notes，而第二个不带。

## 编译环境

### scons & texlive

可以参考 [这里](https://github.com/TimeExceed/water/tree/master/dockerfiles/taoda-base)。

### fathom

如果需要编译绘图，环境中需要有 `fathom` 镜像。
见 [这里](https://github.com/TimeExceed/fathom)。
