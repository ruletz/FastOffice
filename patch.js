const fs = require('fs');
const indexHtmlFile = 'c:\\\\Projects\\\\OnlyOffice\\\\app\\\\index.html';
let content = fs.readFileSync(indexHtmlFile, 'utf8');

// The replacement logic:
const cellRegex = /\{id:"cell",title:utils\.Lang\.newXlsx.*?icon:"#xlsx-big"\}(,|)/g;
const slideRegex = /\{id:"slide",title:utils\.Lang\.newPptx.*?icon:"#pptx-big"\}(,|)/g;
const formRegex = /\{id:"form",title:utils\.Lang\.newForm.*?icon:"#pdf-big"\}(,|)/g;

content = content.replace(cellRegex, '');
content = content.replace(slideRegex, '');
content = content.replace(formRegex, '');

const tab1Regex = /<a data-value='Spreadsheets' class='nav-item'.*?<\/a>/g;
const tab2Regex = /<a data-value='Presentations' class='nav-item'.*?<\/a>/g;
const tab3Regex = /<a data-value='PDFs' class='nav-item'.*?<\/a>/g;

content = content.replace(tab1Regex, '');
content = content.replace(tab2Regex, '');
content = content.replace(tab3Regex, '');

content = content.replace(/Welcome to ONLYOFFICE Desktop Editors!/g, 'Welcome to Word Editor');
content = content.replace(/Create an ONLYOFFICE cloud/g, 'Create a cloud');
content = content.replace(/Work on documents offline or connect the suite to your cloud: ONLYOFFICE, ownCloud, Nextcloud./g, '');
content = content.replace(/ONLYOFFICE/gi, '');

fs.writeFileSync(indexHtmlFile, content);
console.log('Patched index.html successfully!');
Como