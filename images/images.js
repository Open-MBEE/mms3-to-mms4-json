/*jshint esversion: 6 */

const fetch = require('node-fetch');
const jsdom = require('jsdom');
const FormData = require('form-data');
const JSDOM = new jsdom.JSDOM('');
const $ = require('jquery')(JSDOM.window);
const fs = require('fs');

const MMS3TICKET = '';
const MMS3 = 'https://mms.openmbee.org';
const MMS4 = 'https://mms4.openmbee.org';
const USER = ''; //user and pass for mms4
const PASS = '';
const MMS4PROJECTID = '';

// downloads image and uploads it to mms4 as id: name with original ext in filename
async function getImage(url, ext, name) {
    let realurl = (url.indexOf('http') < 0) ? MMS3 + url + "?alf_ticket=" + MMS3TICKET : url;
    let image = await fetch(realurl);
    if (!image.ok) {
        throw 'image ' + realurl + ' error';
    }
    let filename = './downloaded/' + name + '.' + ext;
    let buffer = await image.buffer();
    fs.writeFileSync(filename, buffer);

    let formData = new FormData();
    formData.append('file', fs.createReadStream(filename), filename);
    let upload = await fetch(MMS4 + '/projects/' + MMS4PROJECTID + '/refs/master/elements/' + name, {
        method: 'POST',
        body: formData,
        headers: {'Authorization': 'Basic ' + btoa(USER + ':' + PASS) }
    });
    if (!upload.ok) {
        console.log(upload);
    }
}
async function processImages(htmlin) {
    if (htmlin == 2) {
        console.log('htmlin is 2');
        return '';
    }
    if (!htmlin.includes('<img')) {
        return htmlin;
    }
    let dom = $(htmlin);
    let imgs = dom.find('img');
    for (let i = 0; i < imgs.length; i++) {
        let src = $(imgs[i]).attr('src');
        let index = src.indexOf('/alfresco');
        if (index < 0) {
            continue;
        }
        src = src.substring(index);
        let ticketIndex = src.indexOf('?alf_ticket');
        if (ticketIndex > 0) {
            src = src.substring(0, ticketIndex);
        }
        let srcs = src.split('/');
        let name = srcs[srcs.length-1];
        let ext = name.split('.');
        ext = ext[ext.length-1];
        name = '_hidden_img_' + name.replace(/\./g, '_');
        //console.log(src + ' ' + name + ' ' + ext);
        try {
            await getImage(src, ext, name);
            $(imgs[i]).attr('src', '/projects/' + MMS4PROJECTID + '/refs/master/elements/' + name + '/' + ext);
        } catch(err) {
            console.log('getting image ' + src + ' failed');
        }
    }
    let result = '';
    for (let i = 0; i < dom.length; i++) {
        if (dom[i].outerHTML)
            result += dom[i].outerHTML;
    }
    return result;
}

async function processEl(el) {
    let changed = {id: el.id};
    if (el.documentation) {
        let updated = await processImages(el.documentation);
        if (updated !== el.documentation) {
            changed.documentation = updated;
        }
    }
    if (el.defaultValue && el.defaultValue.value && el.defaultValue.type === 'LiteralString') {
        let updated = await processImages(el.defaultValue.value);
        if (updated !== el.defaultValue.value) {
            changed.defaultValue = el.defaultValue;
            changed.defaultValue.value = updated;
        }
    }
    if (el.value && el.value.length > 0) {
        let slotChanged = false;
        for (let val of el.value) {
            if (val.value && val.type === 'LiteralString') {
                let updated = await processImages(val.value);
                if (val.value !== updated) {
                    val.value = updated;
                    slotChanged = true;
                }
            }
        }
        if (slotChanged) {
            changed.value = el.value;
        }
    }
    return changed;
}

async function processJson() {
    let input = JSON.parse(fs.readFileSync('input.json'));
    let output = [];
    for (let el of input.elements) {
        let changed = await processEl(el);
        if (Object.keys(changed).length > 1) {
            output.push(changed);
        }
    }
    let result = JSON.stringify({elements: output});
    fs.writeFileSync('./processed/output.json', result);
}

processJson();