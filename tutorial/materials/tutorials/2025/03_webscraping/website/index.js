let element = document.querySelector('.link-container');

let tag = document.createElement("p");
let text = document.createTextNode("Added this text with javascript");

tag.appendChild(text);
tag.style.color = 'green'
element.appendChild(tag);
