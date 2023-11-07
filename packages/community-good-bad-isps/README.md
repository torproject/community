# lektor-communit-good-bad-isps plugin

This plugin provides some functions specific to Community website's Good Bad
ISP page, hosted at https://community.torproject.org//relay/community-resources/good-bad-isps/

## Build flags

Extra build flags can be passed to the `lektor build` command via the `-f`
switch to alter the build process. Example: `lektor build -f generate-cw-fractions`.

### `generate-cw-fractions`

This flag will connect to the `metrics.torproject.org` webservice and use the
online data to generate consensus weight fractions, which are a representation
of a particular ASN's contribution to overall relay bandwidth.

An Internet connection is required for this flag to work, otherwise the build
will fail.

If the flag is not used, the Good Bad ISPs page will display `n/a` in that
column.
