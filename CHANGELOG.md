# Changelog

### [0.16.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.16.1...v0.16.2) (2021-07-30)


### Bug Fixes

* updated failed files cron job ([c6e59e1](https://www.github.com/licenseware/licenseware-sdk/commit/c6e59e1df9503578c2cc162e54516f4775bc63b6))

### [0.16.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.16.0...v0.16.1) (2021-07-30)


### Bug Fixes

* added back app_id param to tenant id for backward compatibility ([50f7d98](https://www.github.com/licenseware/licenseware-sdk/commit/50f7d9834ed59c2c7ceecb8ae5595e1749e66bff))
* refactored tenant utils to solve circular import error ([ab105cc](https://www.github.com/licenseware/licenseware-sdk/commit/ab105cc60efe4036dd963ef7efdf2b7557071e9b))

## [0.16.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.15.0...v0.16.0) (2021-07-29)


### Features

* added cron_jobs for background worker, now each 60 minutes will check for timed out files ([31aee4f](https://www.github.com/licenseware/licenseware-sdk/commit/31aee4f804a8ef97e38bb654505a3b78ef8c2943))


### Bug Fixes

* added custom filename exception for odb reviewlite files ([c9be085](https://www.github.com/licenseware/licenseware-sdk/commit/c9be0850099aae3efbe54cac4ea9745edbd97a2c))
* changed beta_flag to flags, fixed urls for internal use ([88aa88c](https://www.github.com/licenseware/licenseware-sdk/commit/88aa88c61b18e9e37c4cc5c499bc8021ff5a06c1))
* mongodata threadsafe ([e439ca9](https://www.github.com/licenseware/licenseware-sdk/commit/e439ca92b253a9b595a09e2a45cdb72f5a4a0832))
* removed /uploads/history route from app creator ([62f2723](https://www.github.com/licenseware/licenseware-sdk/commit/62f2723602d9be5d851f67ebf24b753838d80c51))
* renamed beta_flag to flag in app_definition, added tenant_id param to tenant_utils/get tenants activated and with data, added tenant_registration_url to app creator ([39d8eee](https://www.github.com/licenseware/licenseware-sdk/commit/39d8eee35a84246b2de7a3ed3c1992eb75f49480))
* renamed beta_flag to flags on uploader.py ([1cf8d4b](https://www.github.com/licenseware/licenseware-sdk/commit/1cf8d4b3a5fb76631b8f8bc53a7babcf35e48c1f))
* temporary import fix ([e61e173](https://www.github.com/licenseware/licenseware-sdk/commit/e61e1731dc6774ac0ddc432bf3dcb4befb2f5d89))
* tenantutils used the wrong schema for updating AnalysisStatusSchema ([2385cc6](https://www.github.com/licenseware/licenseware-sdk/commit/2385cc6af6dc4a8503095a4b6cec7d89874c1d3d))
* url on app definition had an extra app prefix ([2eaad2f](https://www.github.com/licenseware/licenseware-sdk/commit/2eaad2f15a807951bace2e1758c261ae7201ad26))

## [0.15.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.14.5...v0.15.0) (2021-07-23)


### Features

* added notifications directly in sdk ([20212a4](https://www.github.com/licenseware/licenseware-sdk/commit/20212a427f316125bc5b58cb9dc651704d1c0c5f))
* get processing status based on uploader ([e4e9db7](https://www.github.com/licenseware/licenseware-sdk/commit/e4e9db768e2992f0c2c249e98a8e147bbf23db71))


### Bug Fixes

* make mongodata thread safe by closing the connection after query ([1981936](https://www.github.com/licenseware/licenseware-sdk/commit/1981936e9e5a8cb26e88966bdd0d57e6eb55faf9))
* notification imports fix ([f63501e](https://www.github.com/licenseware/licenseware-sdk/commit/f63501e36bed381ea3a39e103cb84a1b36ff18f8))

### [0.14.5](https://www.github.com/licenseware/licenseware-sdk/compare/v0.14.4...v0.14.5) (2021-07-16)


### Bug Fixes

* changed order in backward compatibility ([d7cdf3b](https://www.github.com/licenseware/licenseware-sdk/commit/d7cdf3bab779ca653b53d03eec6949025ae25632))

### [0.14.4](https://www.github.com/licenseware/licenseware-sdk/compare/v0.14.3...v0.14.4) (2021-07-14)


### Bug Fixes

* fix in case args were given on notify_status ([f8a937e](https://www.github.com/licenseware/licenseware-sdk/commit/f8a937e6a792a1dba3d7e10944bd3023ead68343))

### [0.14.3](https://www.github.com/licenseware/licenseware-sdk/compare/v0.14.2...v0.14.3) (2021-07-14)


### Bug Fixes

* backward_compatibility for notify_status function params ([d66eb60](https://www.github.com/licenseware/licenseware-sdk/commit/d66eb60d565ed907cd7147183ec335076f7ebd44))

### [0.14.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.14.1...v0.14.2) (2021-07-14)


### Bug Fixes

* import error ([f4da1be](https://www.github.com/licenseware/licenseware-sdk/commit/f4da1be7aae4e2420619d251eb6ca96d294daa37))
* import.. ([6fc7767](https://www.github.com/licenseware/licenseware-sdk/commit/6fc77671fbacb00e71a90fd59b3cf655759c3807))
* relative import fix ([76c5c59](https://www.github.com/licenseware/licenseware-sdk/commit/76c5c59b204f157b68bd2fff2fbf944e72f0d821))

### [0.14.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.14.0...v0.14.1) (2021-07-14)


### Bug Fixes

* updated notify_status to checkmongo for running processes before sending a idle status, log only authentification fail to avoid clutterlogs ([528d78c](https://www.github.com/licenseware/licenseware-sdk/commit/528d78cc42e065103ea763cde5f8fa4d15b96ef8))

## [0.14.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.13.3...v0.14.0) (2021-07-13)


### Features

* notifications decorator for event handler ([cbd3aa1](https://www.github.com/licenseware/licenseware-sdk/commit/cbd3aa16a0a9d791e34b24039dc506ae996dce01))
* notifications decorator for event handler ([aa85eae](https://www.github.com/licenseware/licenseware-sdk/commit/aa85eae0dbbc193b6c5c7ad16267d949e419d613))
* notifications decorator for event handler ([207f59b](https://www.github.com/licenseware/licenseware-sdk/commit/207f59b46ddc4e5f08c87278bf6df91835debab6))
* notifications decorator for event handler ([da129d2](https://www.github.com/licenseware/licenseware-sdk/commit/da129d2a640436f254748f0057b2827653da17e6))
* **redis:** password and db_id are now supported ([d35521c](https://www.github.com/licenseware/licenseware-sdk/commit/d35521c474ae14138656c3e0198006c6ba60514c))


### Bug Fixes

* always ignore case ([16ae307](https://www.github.com/licenseware/licenseware-sdk/commit/16ae307f17141f64e0ca059595c113e4142e1912))
* file_validators flags default to 0 insead of None, mongodata getmongoconnection on getcollection ([2f6b492](https://www.github.com/licenseware/licenseware-sdk/commit/2f6b492c3bdaf9f34af4a8bd8313c12fa58efc4a))
* make notification decorator async ([9a026c4](https://www.github.com/licenseware/licenseware-sdk/commit/9a026c4a05d2ecbe4015230b14cbfdef158b48dd))
* make only wrapped function async ([7cd78bd](https://www.github.com/licenseware/licenseware-sdk/commit/7cd78bd91cf3b62e0a9fa462a87f1cbc89220e57))
* optional ignorecase ([98e5a16](https://www.github.com/licenseware/licenseware-sdk/commit/98e5a167d379e04582c5ad70d762f81835333b7c))
* redis service password optional; auth service create_machine bug ([426fa3f](https://www.github.com/licenseware/licenseware-sdk/commit/426fa3ff5aac79c8f77c6fce06f07f23b79aaff1))
* removed the notifications decorator ([a48b246](https://www.github.com/licenseware/licenseware-sdk/commit/a48b2464f41f77c1c8b152091ea9be6057a8ae76))
* return StrictRedis when using password ([d1f8de1](https://www.github.com/licenseware/licenseware-sdk/commit/d1f8de15baa31278cd4880f137d74d6ac9dee01f))

### [0.13.3](https://www.github.com/licenseware/licenseware-sdk/compare/v0.13.2...v0.13.3) (2021-07-02)


### Bug Fixes

* filename validation is now case insensitive ([ea9b037](https://www.github.com/licenseware/licenseware-sdk/commit/ea9b037b869e07f907d7739d0e2a30d9fd49ae34))

### [0.13.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.13.1...v0.13.2) (2021-07-02)


### Bug Fixes

* moved stream cursor to 0 on file_validator ([9e133cc](https://www.github.com/licenseware/licenseware-sdk/commit/9e133ccece3915e946888ad70034d1ac4c2144df))

### [0.13.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.13.0...v0.13.1) (2021-07-01)


### Bug Fixes

* stream decode errors ([2c9ca28](https://www.github.com/licenseware/licenseware-sdk/commit/2c9ca287317442965d36d6078f2f395e270f96b8))

## [0.13.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.12.1...v0.13.0) (2021-07-01)


### Features

* added history url to app definition ([e6b4f9c](https://www.github.com/licenseware/licenseware-sdk/commit/e6b4f9c86d9dbf694230749235fe441a535b0a04))

### [0.12.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.12.0...v0.12.1) (2021-07-01)


### Bug Fixes

* resource var overwrite issue ([80b28cc](https://www.github.com/licenseware/licenseware-sdk/commit/80b28cc16e45a44aeeeb399ee46eef6c2e087c77))

## [0.12.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.11.0...v0.12.0) (2021-06-30)


### Features

* added reports to app_creator, now all urls related to app definition, reports, uploads are created from dictionaries ([a3c337f](https://www.github.com/licenseware/licenseware-sdk/commit/a3c337f986a884b821a9fb73793fe4843d56a370))

## [0.11.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.10.0...v0.11.0) (2021-06-29)


### Features

* added quota for sccm ([0f96afd](https://www.github.com/licenseware/licenseware-sdk/commit/0f96afd57ab4e3f17c7e905f1da3644ded84cb71))

## [0.10.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.9.0...v0.10.0) (2021-06-29)


### Features

* added icon to StandardReportComponent ([0363bc2](https://www.github.com/licenseware/licenseware-sdk/commit/0363bc2b6140ee61a4c6760539fb1a97984e0381))

## [0.9.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.8.1...v0.9.0) (2021-06-28)


### Features

* added powercli quota ([d358450](https://www.github.com/licenseware/licenseware-sdk/commit/d358450e6993ea3f35c9a3cfef6d7ac8456fcca6))

### [0.8.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.8.0...v0.8.1) (2021-06-28)


### Bug Fixes

* re.IGNORE caused issues on file_validator ([0688260](https://www.github.com/licenseware/licenseware-sdk/commit/068826032aa1d7a8ee57ddd6fab209dc86fb33a3))

## [0.8.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.7.2...v0.8.0) (2021-06-28)


### Features

* made uploader url parameters optional ([2f10d40](https://www.github.com/licenseware/licenseware-sdk/commit/2f10d402d6506b43b66e98d27b5aad0a26d86513))

### [0.7.2](https://www.github.com/licenseware/licenseware-sdk/compare/v0.7.1...v0.7.2) (2021-06-28)


### Bug Fixes

* namespace generator generates now only specified http methods ([72f65b9](https://www.github.com/licenseware/licenseware-sdk/commit/72f65b96ef5eaa90c27cbb55baf3be9a08c059b5))

### [0.7.1](https://www.github.com/licenseware/licenseware-sdk/compare/v0.7.0...v0.7.1) (2021-06-28)


### Bug Fixes

* added flask request on service method, moved report initialization in class instantiation ([719efda](https://www.github.com/licenseware/licenseware-sdk/commit/719efda379b892de27be74c168bcfc1a1531f9b2))

## [0.7.0](https://www.github.com/licenseware/licenseware-sdk/compare/v0.6.2...v0.7.0) (2021-06-25)


### Features

* added beta_flag to registration payload ([070d428](https://www.github.com/licenseware/licenseware-sdk/commit/070d428f9680aaf0271cb3cdc9fee78df707137d))

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
