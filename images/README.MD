`npm install`

download project elements json from mms4, save into input.json in this dir

`
curl -X GET -u user http://mms4.server/projects/projectId/refs/master/elements > input.json
`

create 'downloaded' and 'processed' folders if they don't exist

update images.js with mms4 project id, mms3 ticket, mms4 user/pass

run node images.js

`node images.js`

downloaded images will be in ./downloaded/ folder, post ./processed/output.json to mms4 project

`
curl -X POST -u user -H 'Content-Type: application/json' -d @processed/output.json http://mms4.server/projects/projectId/refs/master/elements 
`
