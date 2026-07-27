# Course v2 reconstruction diagnostic

## Part inventory
.remediation/course-v2.part00 bytes=5000 compact_chars=5000 prefix=H4sIAAAAAAAAA+w8a4/bRpL+ suffix=cg5bmhkFzC8nwYE5NbbLR2Gy
.remediation/course-v2.part01 bytes=10000 compact_chars=10000 prefix=nGn+xVIrRi/pFssjEkx3lFX/ suffix=HR2cGpMnRWl44l1SvSJ59CuU
.remediation/course-v2.part02 bytes=10000 compact_chars=10000 prefix=5FCUVTgFo6YfsERP0IVAYuSG suffix=7bgsSIFG5tioAWSVtItUZ/Ch
.remediation/course-v2.part03 bytes=10000 compact_chars=10000 prefix=HvCZ6F4a+wUdW/viox1gjtFV suffix=AJ4BY6BVwNletsTOFtpcMhYV
.remediation/course-v2.part04 bytes=15000 compact_chars=15000 prefix=hl5B2SJlkPlv2TPHGWNhUeit suffix=y0nW+fuV2R5/vj/NofxIajrp

## Combined-stream errors
### /tmp/base64-stream.err
### /tmp/gzip-stream.err

gzip: /tmp/course-v2.tar.gz: unexpected end of file

## Per-part decode
.remediation/course-v2.part00 decoded_bytes=3750 first_hex=1f8b080000000000
.remediation/course-v2.part01 decoded_bytes=7500 first_hex=9c69fec5522b462f
.remediation/course-v2.part02 decoded_bytes=7500 first_hex=e45094553805a3a6
.remediation/course-v2.part03 decoded_bytes=7500 first_hex=1ef099e85e1afb05
.remediation/course-v2.part04 decoded_bytes=11250 first_hex=865e41d9226590f9

## Concatenated binary
/tmp/diagnostic-concatenated.bin: gzip compressed data, from Unix, original size modulo 2^32 3912919624 gzip compressed data, unknown method, ASCII, was "", encrypted, from FAT filesystem (MS-DOS, OS/2, NT), original size modulo 2^32 3912919624

gzip: /tmp/diagnostic-concatenated.bin: unexpected end of file
bytes=37500
