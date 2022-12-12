'use strict';

let resourceFilters = {
  topic: document.getElementById('topicDropdownMenuButton').dataset.currentValue || null,
  lang: document.getElementById('languageDropdownMenuButton').dataset.currentValue || null,
  author: document.getElementById('authorDropdownMenuButton').dataset.currentValue || null,
};

let resources = document.querySelectorAll('#resource-list > .resource-list-entry');
let topic_dropdown_button = document.getElementById('topicDropdownMenuButton');
let lang_dropdown_button = document.getElementById('languageDropdownMenuButton');
let author_dropdown_button = document.getElementById('authorDropdownMenuButton');

const translatedTopic = document.currentScript.getAttribute('topic');
const translatedTopicColon = document.currentScript.getAttribute('topic-colon');
const translatedLang = document.currentScript.getAttribute('lang');
const translatedLangColon = document.currentScript.getAttribute('lang-colon');
const translatedAuthor = document.currentScript.getAttribute('author');
const translatedAuthorColon = document.currentScript.getAttribute('author-colon');

function setTopic(ev) {
  ev.preventDefault();

  let topic = ev.target.dataset.topic;
  let topicReadable = ev.target.innerText;
  let newText = `${translatedTopicColon} ${topicReadable}`;

  if (topic === 'none') { 
    topic = null;
    newText = translatedTopic;
  }

  topic_dropdown_button.innerText = newText;
  resourceFilters.topic = topic;
}

function setLang(ev) {
  ev.preventDefault();

  let lang = ev.target.dataset.lang;
  let langReadable = ev.target.innerText;
  let newText = `${translatedLangColon} ${langReadable}`;

  if (lang === 'none') {
    lang = null;
    newText = translatedLang;
  }

  lang_dropdown_button.innerText = newText;
  resourceFilters.lang = lang;
}

function setAuthor(ev) {
  ev.preventDefault();

  let author = ev.target.dataset.author;
  let authorReadable = ev.target.innerText;
  let newText = `${translatedAuthorColon} ${authorReadable}`;

  if (author === 'none') {
    author = null;
    newText = translatedAuthor;
  }

  resourceFilters.author = author;
  author_dropdown_button.innerText = newText;
}

function applyFilters(topic, lang, author) {
  const hide = element => element.classList.add('d-none');
  const unhide = element => element.classList.remove('d-none');

  resources.forEach(resource => {
    let hidden = false;
    if (topic && !resource.dataset.topics.includes(`:${topic}:`)) {
        console.log('topic');
      hide(resource);
    } else if (lang && !resource.dataset.langs.includes(`:${lang}:`)) {
        console.log(`dataset does not include selected lang: :${lang}:`);
      hide(resource);
    } else if (author && resource.dataset.author != author) {
        console.log('author');
      hide(resource);
    } else {
      unhide(resource);
    }
  });
}

document.querySelectorAll('.filterApplyButton').forEach(button => {
  button.classList.remove('d-none');
  button.addEventListener('click', ev => {
    applyFilters(resourceFilters.topic, resourceFilters.lang, resourceFilters.author);
  });
});
