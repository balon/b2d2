from subprocess import call

accID = "6174650cbcda"
appID = "001361378b8aafd87ae9c2cc0b62b96f77dcc8f4e2"
bucket = "b2d2test"
path = "/Users/balon/Desktop/cherger.pgm"

call(["b2", "authorize-account", accID, appID])
call(["b2", "upload-file", "--threads", "10", bucket, path, "paths/test" ])