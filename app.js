// app.js — small client-side app to render books and resources
async function loadBooks(){
  try{
    const res = await fetch('data/books.json');
    const books = await res.json();
    return books;
  }catch(e){
    console.error('Failed to load books', e);
    return [];
  }
}

function el(tag, attrs = {}, ...children){
  const node = document.createElement(tag);
  for(const k in attrs){
    if(k.startsWith('on') && typeof attrs[k] === 'function') node.addEventListener(k.slice(2).toLowerCase(), attrs[k]);
    else if(k === 'html') node.innerHTML = attrs[k];
    else node.setAttribute(k, attrs[k]);
  }
  for(const c of children){ if(typeof c === 'string') node.appendChild(document.createTextNode(c)); else if(c) node.appendChild(c); }
  return node;
}

function renderBookCard(book){
  const card = el('article',{class:'card'});
  const cover = el('div',{class:'cover',style:`background-image:url(${book.cover})`});
  const title = el('h4',{class:'title'},book.title);
  const author = el('div',{class:'author'},book.author);
  const desc = el('p',{style:'font-size:0.95rem;color:#333;margin:8px 0 0;'},book.short || book.description.slice(0,130) + '...');
  const tags = el('div',{class:'tags'});
  (book.tags||[]).forEach(t=>tags.appendChild(el('span',{class:'tag'},t)));
  const btn = el('button',{onClick:()=>openModal(book)},'Details');
  card.append(cover,title,author,desc,tags,btn);
  return card;
}

function openModal(book){
  const modal = document.getElementById('modal');
  const body = document.getElementById('modalBody');
  body.innerHTML = '';
  const cover = el('div',{class:'cover',style:`background-image:url(${book.cover});height:320px;margin-bottom:12px`});
  const title = el('h2',{},book.title);
  const author = el('div',{class:'author'},book.author);
  const p = el('p',{style:'white-space:pre-line;margin-top:12px'},book.description);
  const buy = el('a',{href:book.buyLink||'#',target:'_blank',class:'btn',style:'display:inline-block;margin-top:12px'},'Buy / Learn more');
  body.append(cover,title,author,p,buy);
  modal.classList.remove('hidden');
  modal.setAttribute('aria-hidden','false');
}

function closeModal(){
  const modal = document.getElementById('modal');
  modal.classList.add('hidden');
  modal.setAttribute('aria-hidden','true');
}

function applySearch(books, query){
  if(!query) return books;
  const q = query.toLowerCase().trim();
  return books.filter(b=>{
    return (b.title && b.title.toLowerCase().includes(q)) ||
           (b.author && b.author.toLowerCase().includes(q)) ||
           (b.tags && b.tags.join(' ').toLowerCase().includes(q)) ||
           (b.description && b.description.toLowerCase().includes(q));
  });
}

(async function init(){
  const books = await loadBooks();
  const grid = document.getElementById('booksGrid');
  const search = document.getElementById('search');

  function refresh(){
    const q = search.value;
    const list = applySearch(books,q);
    grid.innerHTML = '';
    if(list.length===0) grid.appendChild(el('div',{},'No books found.'));
    list.forEach(b=>grid.appendChild(renderBookCard(b)));
  }

  search.addEventListener('input',()=>refresh());
  document.getElementById('closeModal').addEventListener('click',closeModal);
  document.getElementById('modal').addEventListener('click',(e)=>{ if(e.target.id==='modal') closeModal(); });

  refresh();
})();
