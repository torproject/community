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

// set the initial state, for our history api manipulation
history.replaceState(resourceFilters, '', window.location.pathname);

Array.from(document.getElementsByClassName('onclick-setTopic'))
  .forEach(el => el.addEventListener('click', event => {
    event.preventDefault()

    let topic = event.target.dataset.topic;
    let topicReadable = event.target.innerText;

    setTopic(topic, topicReadable);
  }));

Array.from(document.getElementsByClassName('onclick-setLang'))
  .forEach(el => el.addEventListener('click', event => {
    event.preventDefault()

    let lang = event.target.dataset.lang;
    let langReadable = event.target.innerText;

    setLang(lang, langReadable);
  }));

Array.from(document.getElementsByClassName('onclick-setAuthor'))
  .forEach(el => el.addEventListener('click', event => {
    event.preventDefault()

    let author = event.target.dataset.author;
    let authorReadable = event.target.innerText;

    setAuthor(topic, topicReadable);
  }));

function setTopic(topic, topicReadable) {
  let newText = `${translatedTopicColon} ${topicReadable}`;

  if (topic === 'none' || topic === null) {
    topic = null;
    newText = translatedTopic;
  }

  topic_dropdown_button.innerText = newText;
  resourceFilters.topic = topic;
}

function setLang(lang, langReadable) {
  let newText = `${translatedLangColon} ${langReadable}`;

  if (lang === 'none' || lang === null) {
    lang = null;
    newText = translatedLang;
  }

  lang_dropdown_button.innerText = newText;
  resourceFilters.lang = lang;
}

function setAuthor(author, authorReadable) {
  let newText = `${translatedAuthorColon} ${authorReadable}`;

  if (author === 'none' || author === null) {
    author = null;
    newText = translatedAuthor;
  }

  resourceFilters.author = author;
  author_dropdown_button.innerText = newText;
}

function applyFilters(topic, lang, author, modifyHistory=true) {
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

  if (modifyHistory) {
    let filters = {'topic': topic, 'lang': lang, 'author': author};
    setNewSortUrl(filters);
  }
}

function buildNewUrl(currentUrl, filters) {
  if (currentUrl.slice(-1) == '/') {
    currentUrl = currentUrl.slice(0, -1);
  }

  let baseUrl = currentUrl.split('/').slice(0, -3).join('/');

  let topic = filters.topic || 'none';
  let lang = filters.lang || 'none';
  let author = filters.author || 'none';

  return `${baseUrl}/${topic}/${lang}/${author}/`;
}

function setNewSortUrl(filters) {
  let newUrl = buildNewUrl(window.location.pathname, filters);
  history.pushState(filters, '', newUrl);
}

document.querySelectorAll('.filterApplyButton').forEach(button => {
  button.classList.remove('d-none');
  button.addEventListener('click', ev => {
    applyFilters(resourceFilters.topic, resourceFilters.lang, resourceFilters.author);
  });
});

window.addEventListener('popstate', event => {
  event.preventDefault();

  let topicReadable = null;
  let langReadable = null;
  let authorReadable = null;
  
  if (event.state.topic) {
    topicReadable = document.querySelector(`div[aria-labelledby=topicDropdownMenuButton] a[data-topic=${event.state.topic}]`).innerText;
  }
  if (event.state.lang) {
    langReadable = document.querySelector(`div[aria-labelledby=languageDropdownMenuButton] a[data-lang=${event.state.lang}]`).innerText;
  }
  if(event.state.author) {
    authorReadable = document.querySelector(`div[aria-labelledby=authorDropdownMenuButton] a[data-author=${event.state.author}]`).innerText;
  }

  setTopic(event.state.topic, topicReadable);
  setLang(event.state.lang, langReadable);
  setAuthor(event.state.author, authorReadable);

  applyFilters(event.state.topic, event.state.lang, event.state.author, false)
});
