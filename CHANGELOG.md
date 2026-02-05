# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [2.0.0](https://github.com/yaph/wim/releases/tag/2.0.0) - 2026-02-02

<small>[Compare with 1.2.0](https://github.com/yaph/wim/compare/1.2.0...2.0.0)</small>

### Added

- Add qax script to run qa checks with not required packages ([3266260](https://github.com/yaph/wim/commit/32662603c592e622942f2c94add2cdfe21dbf457) by Ramiro Gómez).
- Add wim/extract_exifdata.py script. ([76579e2](https://github.com/yaph/wim/commit/76579e209a9ed546d389cd601ee37ead6d949433) by Ramiro Gómez).
- Add type annotations ([736114e](https://github.com/yaph/wim/commit/736114e4031808317ce11568f6b572f279e88479) by Ramiro Gómez).
- Add and edit function documentation. ([a329f43](https://github.com/yaph/wim/commit/a329f435d50c79ecc4edb45cdfcfc6ddee6af6b3) by Ramiro Gómez).
- Add --trim argument ([10bb52d](https://github.com/yaph/wim/commit/10bb52df201d5de04bdbf299e7f7d04d1bd511fb) by Ramiro Gómez).
- Add --quality argument for setting the image quality ([1fb9b6d](https://github.com/yaph/wim/commit/1fb9b6d11ab29d1bade84dc2792157f62d932912) by Ramiro Gómez).
- Add --strip argument for removing metadata ([17389ea](https://github.com/yaph/wim/commit/17389ea96c3368225ad968b331e76d37859c5697) by Ramiro Gómez).
- Add version argument ([422c6bb](https://github.com/yaph/wim/commit/422c6bb2d876c6664918744387cdd24c290e48ea) by Ramiro Gómez).
- Add complexipy and skylos to qa script ([3545afd](https://github.com/yaph/wim/commit/3545afdecc4f6d3c2b00689ea1928a1ff0591b38) by Ramiro Gómez).

### Fixed

- Fix argument name in test ([922328e](https://github.com/yaph/wim/commit/922328ef4e3b36afb8fc4e304f2b122e1f8d44d4) by Ramiro Gómez).
- fix: Retain metadata such as GPS location of original image ref: Reduce complexity of cli:main function fix: Center text on text image overlay fix: Apply font size when default font is used ([ffb8ad5](https://github.com/yaph/wim/commit/ffb8ad5311cec66a6d8ab6ca77bae4dea02b51d1) by Ramiro Gómez).

### Changed

- Change skylos call ([ddd7e4e](https://github.com/yaph/wim/commit/ddd7e4e8da6bebca4b53dab35dadd09719967cc4) by Ramiro Gómez).

### Removed

- Remove default --font-size and require --font when setting size. ([5c0358c](https://github.com/yaph/wim/commit/5c0358c7f43a24fd1efd0c8dfea56c822bdef8d2) by Ramiro Gómez).
- Remove -q option ([9be4eab](https://github.com/yaph/wim/commit/9be4eabddb10040b5a7a72c78f66b307a369f4c8) by Ramiro Gómez).

## [1.2.0](https://github.com/yaph/wim/releases/tag/1.2.0) - 2025-12-29

<small>[Compare with 1.1.0](https://github.com/yaph/wim/compare/1.1.0...1.2.0)</small>

### Fixed

- Fix typing issues ([5ae06aa](https://github.com/yaph/wim/commit/5ae06aaacb585e31f93df8cb08e04122f6679ebc) by Ramiro Gómez).
- Fix issues with EXIF orientation when adding text or watermark images. ([11ee5f1](https://github.com/yaph/wim/commit/11ee5f1c38df87eb596030dcc2e868192513e3aa) by Ramiro Gómez).

### Removed

- Remove arial as default font and load library default. Gracefully handle missing fonts if specified. ([716f7b8](https://github.com/yaph/wim/commit/716f7b84e9dc633961addd9d158b5463a4fe7c02) by Ramiro Gómez).

## [1.1.0](https://github.com/yaph/wim/releases/tag/1.1.0) - 2025-12-29

<small>[Compare with 1.0.0](https://github.com/yaph/wim/compare/1.0.0...1.1.0)</small>

### Added

- Add outdir argument and prevent clashes between mutually exclusive arguments. ([a9660d1](https://github.com/yaph/wim/commit/a9660d194b7ed63fdd0971ae99138cfd28e38f0f) by Ramiro Gómez).
- Add support for processing multiple input images. Use thumbnail function for all scaling operations. Bumb version. ([33db127](https://github.com/yaph/wim/commit/33db1274d8fbbaa8a9d494c416853eca8a4c6f57) by Ramiro Gómez).

## [1.0.0](https://github.com/yaph/wim/releases/tag/1.0.0) - 2025-12-28

<small>[Compare with 0.2.1](https://github.com/yaph/wim/compare/0.2.1...1.0.0)</small>

### Added

- Add tests ([0ae6c21](https://github.com/yaph/wim/commit/0ae6c2197f08cf38ea2bc860763ec00d93e52b70) by Ramiro Gómez).
- add .github ([5539e22](https://github.com/yaph/wim/commit/5539e22be0d9f01a41ff0b8362f85960536a8998) by Ramiro Gómez).

## [0.2.1](https://github.com/yaph/wim/releases/tag/0.2.1) - 2015-06-27

<small>[Compare with 0.2.0](https://github.com/yaph/wim/compare/0.2.0...0.2.1)</small>

## [0.2.0](https://github.com/yaph/wim/releases/tag/0.2.0) - 2015-06-25

<small>[Compare with first commit](https://github.com/yaph/wim/compare/6ef6eb7609e1172afec97634365ae0ada01e8d98...0.2.0)</small>

### Added

- added markup ([3b55078](https://github.com/yaph/wim/commit/3b55078b40d0d81648fb7db16bb37dfe8e43cb97) by Ramiro Gómez).
- Added help texts for arguments. ([d5f0f56](https://github.com/yaph/wim/commit/d5f0f56a49810523489f6b3d8cf52c872a47b4ff) by Ramiro Gómez).
- Added `scale` and `quantize` options to determine image size and quality. ([e3fdc80](https://github.com/yaph/wim/commit/e3fdc8085ccf152a74dc678205a3fd9f952c1579) by Ramiro Gómez).
- Add text directly to image instead of composing 2 images. Include requirements in setup.py. Added install task. ([dbdf016](https://github.com/yaph/wim/commit/dbdf016635ece8dc9cdaa415aa8d0378434fd436) by Ramiro Gómez).
- added inplace argument and removed text transparency ([189dd1d](https://github.com/yaph/wim/commit/189dd1d6a3f7a8aa5418412014543aabc0f492cf) by Ramiro Gómez).
- added fontsize and text options ([898749a](https://github.com/yaph/wim/commit/898749a8a2b0aec0655332347f85f92c93381a47) by Ramiro Gómez).
- added wim command to setup ([c0bb1ac](https://github.com/yaph/wim/commit/c0bb1ac4224042d2466cd1bc30483d0e55b229c5) by Ramiro Gómez).

### Fixed

- fixed markup ([a66d323](https://github.com/yaph/wim/commit/a66d323676e3f009ade19800e2509249875135b9) by Ramiro Gómez).
- fix rst ([dc6c236](https://github.com/yaph/wim/commit/dc6c2366060957b32985435860faaba28ed748e0) by Ramiro Gómez).
- Fixed #3: description and usage example. ([e4d8d37](https://github.com/yaph/wim/commit/e4d8d3794dab08a3f0a513ea84170f3e165ad639) by Ramiro Gómez).
- fixed syntax error in setup.py and automate docs release ([c2e4ab5](https://github.com/yaph/wim/commit/c2e4ab50b73b2ece4f00a2d3002ad642dade8431) by Ramiro Gómez).

### Removed

- removed unavailable badge ([fde6cf3](https://github.com/yaph/wim/commit/fde6cf34c99d0b48da586b64820107909a79cac0) by Ramiro Gómez).
- Removed generated docs. ([594fb21](https://github.com/yaph/wim/commit/594fb2155307f8836c1be5fe2c7b877464b8b6b4) by Ramiro Gómez).

