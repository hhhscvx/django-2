const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
// данные css файла bookmarklet.css
const minWidth = 250;
// Минимальные значения для изображений
const minHeight = 250;

var head = document.getElementsByTagName('head')[0];
// Подключаем css
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
// <link rel="stylesheet" type="text/css">
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);
// Добавляем <link> d head

var body = document.getElementsByTagName('body')[0];
boxHtml = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Выберите картинку для сохранения:</h1>
    <div class="images"></div>
  </div>`;
body.innerHTML += boxHtml;
// Добавляем в body верхний <div>

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');

    imagesFound.innerHTML = '';
    // очистить найденные изображения перед загрузкой новых
    bookmarklet.style.display = 'block';
    // показать букмарклет
    // событие закрытия; По клику на close(x) - дисплей букмарклета становится none
    bookmarklet.querySelector('#close')
             .addEventListener('click', function(){
    bookmarklet.style.display = 'none'
    });

    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach(image => {
    if(image.naturalWidth >= minWidth
       && image.naturalHeight >= minHeight)
    {
      var imageFound = document.createElement('img');
      imageFound.src = image.src;
      imagesFound.append(imageFound);
    }
  })
  imagesFound.querySelectorAll('img').forEach(image => {
    image.addEventListener('click', function(event){
      imageSelected = event.target;
      bookmarklet.style.display = 'none';
      window.open(siteUrl + 'images/create/?url='
                  + encodeURIComponent(imageSelected.src)
                  + '&title='
                  + encodeURIComponent(document.title),  // title берется с тайтла страницы
                  '_blank');
    })
  })
}

bookmarkletLaunch(); // запустить букмарклет