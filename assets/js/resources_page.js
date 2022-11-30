'use strict';

window.resourceFilters = {
  topic: null,
  lang: null,
  author: null,
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
  window.resourceFilters.topic = topic;
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
  window.resourceFilters.lang = lang;
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

  window.resourceFilters.author = author;
  author_dropdown_button.innerText = newText;
}

function applyFilters(topic, lang, author) {
  const hide = element => element.classList.add('d-none');
  const unhide = element => element.classList.remove('d-none');

  resources.forEach(resource => {
    let hidden = false;
    if (topic && !resource.dataset.topics.includes(`:${topic}:`)) {
      hide(resource);
    } else if (lang && !resource.dataset.langs.includes(`:${lang}:`)) {
      hide(resource);
    } else if (author && resource.dataset.author != author) {
      hide(resource);
    } else {
      unhide(resource);
    }
  });
}

document.querySelectorAll('.filterApplyButton').forEach(button => {
  button.classList.remove('d-none');
  button.addEventListener('click', ev => {
    applyFilters(window.resourceFilters.topic, window.resourceFilters.lang, window.resourceFilters.author);
  });
});
