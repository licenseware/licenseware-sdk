# Changelog

### [0.6.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.6.1...v0.6.2) (2021-06-25)


### Bug Fixes

* added notify_registry to Uploader ([164c307](https://www.github.com/licenseware/licenseware-sdk/commit/164c307beae3241dd90a3bebd732a4335176e30b))

### [0.6.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.6.0...v0.6.1) (2021-06-25)


### Bug Fixes

* forgot report init ([0912735](https://www.github.com/licenseware/licenseware-sdk/commit/09127350f72cb8826f72552abb45b07e8cc86b08))

## [0.6.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.5.3...v0.6.0) (2021-06-25)


### Features

* added ReportCreator which generates the restx api from given data ([8e39a35](https://www.github.com/licenseware/licenseware-sdk/commit/8e39a353fb5ef64c372b9c7685dde2200382e865))
* automatically get wheel version from CHANGELOG ([0174683](https://www.github.com/licenseware/licenseware-sdk/commit/0174683b40c728b17bb3b1e2b79f31f8185a3900))

### [0.5.3](https://www.github.com/licenseware/licenseware-sdk/compare/v0.5.2...v0.5.3) (2021-06-23)


### Bug Fixes

* added authentication to notifications from workers ([71108a3](https://www.github.com/licenseware/licenseware-sdk/commit/71108a39c54c692a80a2aab52545a13d39f437b6))

### [0.5.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.5.1...v0.5.2) (2021-06-22)


### Bug Fixes

* AppCreator issues fixed ([9e37fef](https://www.github.com/licenseware/licenseware-sdk/commit/9e37fefdbf585fe3a251ed096ebb39037484cc2f))

### [0.5.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.5.0...v0.5.1) (2021-06-22)


### Bug Fixes

* removed dependency clutter ([f270ab5](https://www.github.com/licenseware/licenseware-sdk/commit/f270ab5b142275bc3977956b39825b9c2e2ff2b0))

## [0.5.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.4.1...v0.5.0) (2021-06-22)


### Features

* added AppCreator which allows register of uploder, history, quota, app_definition all in one go ([0aae36a](https://www.github.com/licenseware/licenseware-sdk/commit/0aae36ad015943f63d2920ee8d027f6ebad54d31))


### Bug Fixes

* revert to mongodata module to solve imports ([b536b9a](https://www.github.com/licenseware/licenseware-sdk/commit/b536b9a7c3e7a6c8bb2c5808022a605457df9a78))


### Documentation

* added docs for AppCreator ([62ddefc](https://www.github.com/licenseware/licenseware-sdk/commit/62ddefc17d44bdf553758ec926552b8289283bd6))

### [0.4.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.4.0...v0.4.1) (2021-06-21)


### Bug Fixes

* auto refresh token before every request ([ba830d9](https://www.github.com/licenseware/licenseware-sdk/commit/ba830d9636083e78bf3965ca8b04303ab77aafc6))
* fix relative import ([b9a561f](https://www.github.com/licenseware/licenseware-sdk/commit/b9a561f97d285c38f789e4550f1e10f3ef46e5b4))
* fixed relative import for mongodata ([ceaa765](https://www.github.com/licenseware/licenseware-sdk/commit/ceaa7659fe5b83549df9bbebdb80d82bd4965e93))

## [0.4.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.3.4...v0.4.0) (2021-06-18)


### Features

* added google document AI sdk ([602cb73](https://www.github.com/licenseware/licenseware-sdk/commit/602cb73040f6163cb758fa506b8f4c5c689324be))

### [0.3.4](https://www.github.com/licenseware/licenseware-sdk/compare/v0.3.3...v0.3.4) (2021-06-16)


### Bug Fixes

* droped dups changes, mongo doesn't preserve field order ([e34aabd](https://www.github.com/licenseware/licenseware-sdk/commit/e34aabdece2151caead9a0ebf783c370c4d7b073))

### [0.3.3](https://www.github.com/licenseware/licenseware-sdk/compare/v0.3.2...v0.3.3) (2021-06-16)


### Bug Fixes

* duplicates on list of objects ([e58ff14](https://www.github.com/licenseware/licenseware-sdk/commit/e58ff148e7049390e6e4ed5e5d0cb3798577787d))

### [0.3.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.3.1...v0.3.2) (2021-06-15)


### Bug Fixes

* removed test setup ([097b545](https://www.github.com/licenseware/licenseware-sdk/commit/097b545ea315d11d05c7ae81854384a63520a552))

### [0.3.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.3.0...v0.3.1) (2021-06-15)


### Bug Fixes

* mongodata with append on list of dicts created duplicates, added a pipeline to remove duplicates if field with with list of dicts is found ([a126427](https://www.github.com/licenseware/licenseware-sdk/commit/a1264276a884043c57af3718e1630cbcad60b089))

## [0.3.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.2.0...v0.3.0) (2021-06-10)


### Features

* added pandas-dedupe dependency ([ab3f1a2](https://www.github.com/licenseware/licenseware-sdk/commit/ab3f1a297151f1c5659cf56bb4cf0418e2d8ccba))

## [0.2.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.1.4...v0.2.0) (2021-06-09)


### Features

* added dedupe library, update by str index mongodata ([32e4114](https://www.github.com/licenseware/licenseware-sdk/commit/32e41142ebbb7ed6c23d3aa55248385f74d06c75))


### Bug Fixes

* removed test setup mongodata ([2988f58](https://www.github.com/licenseware/licenseware-sdk/commit/2988f58e98ec428c5dd07de645cd80e028c4aa2c))

### [0.1.4](https://www.github.com/licenseware/licenseware-sdk/compare/v0.1.3...v0.1.4) (2021-06-08)


### Bug Fixes

* auto refresh token ([69468dd](https://www.github.com/licenseware/licenseware-sdk/commit/69468ddfd4861eb7cb7cbb4282804149284ee66c))

### [0.1.3](https://www.github.com/licenseware/licenseware-sdk/compare/v0.1.2...v0.1.3) (2021-06-03)


### Bug Fixes

* create_index (background=true) was throwing an error ([31dbeab](https://www.github.com/licenseware/licenseware-sdk/commit/31dbeab666d195d96a2df44479a7f9f0cdfdde42))

### [0.1.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.1.1...v0.1.2) (2021-06-03)


### Bug Fixes

* changed create index to use the mongodata collection object ([5530a17](https://www.github.com/licenseware/licenseware-sdk/commit/5530a17b6bbab3fb6dbf9bfab02d85efdcbd2c15))

### [0.1.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.1.0...v0.1.1) (2021-06-03)


### Bug Fixes

* bad comment line ([22f9518](https://www.github.com/licenseware/licenseware-sdk/commit/22f9518770be6eedae7213f826a9e7693c874faf))

## [0.0.12](https://www.github.com/licenseware/licenseware-sdk/compare/v0.0.11...v0.0.12) (2021-06-03)


### Features

* **mongo_crud:** added auto-creation of indexes based on serializer ([8b7d173](https://www.github.com/licenseware/licenseware-sdk/commit/8b7d173a56004848cdea00905176742a4f89ae71))


### Documentation

* added changelog generator ([81ef71e](https://www.github.com/licenseware/licenseware-sdk/commit/81ef71efc4124700c9ff780d9332fbfea6d6007a))
