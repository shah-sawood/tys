document.addEventListener('DOMContentLoaded', function () {
    load_header();  // load header
    load_navbar();  // load nav bar

    // by default load home page
    load_home_page();
});
// months of the year
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// root title for all pages
const title = ' - Test Your Skills';
function load_home_page() {
    // change title to home
    document.querySelector('title').innerText = `Home${title}`;
    const main = document.querySelector('main');
    main.innerHTML = '';

    // create a row for all categories
    const row = document.createElement('div');
    row.setAttribute('id', 'categories');   // give row an id
    row.classList.add('row', 'g-3', 'p-3', 'mx-auto'); // add row classes

    // create a card for each category
    fetch('api/')
    .then(response => response.json())
    .then(result => {
        var auth = "{{ request.user.is_authenticated }}";
        for (let i = 0; i < result.length; i++) {
            const card = create_card(result[i]);
            row.append(card);
        }
    });
    main.append(row);
}

// create a card for category
function create_card(object) {
    // create a column
    const col = document.createElement('div');
    col.classList.add('col-12', 'col-sm-6', 'col-md-4', 'col-lg-4', 'col-xl-3', 'col-xxl-1');

    const card = document.createElement('div');
    card.classList.add('card', 'bg-light', 'mx-auto',);
    setStyle(card, 'width', '18rem');
    card.setAttribute('title', `Click here to visit ${object.name} category`);
    card.setAttribute('onclick', `get_questions(${object.id});`);

    const image = document.createElement('img');
    image.classList.add("card-img-top", "card-image");
    image.setAttribute('alt', `${object.name}`);
    image.setAttribute('src', `${object.image.slice(6)}`);

    const body = document.createElement('div');
    body.classList.add('card-body', 'bg-info');

    const title = document.createElement('h5');
    title.classList.add('card-title');
    title.innerText = `${object.name}`;

    const card_text = document.createElement('p');
    card_text.classList.add('card-text');

    const questions = document.createElement('div');
    questions.innerText = `Questions: ${object.questions.length}`;

    const updated = document.createElement('div');
    var date = new Date(object.updated);
    updated.innerText = `Updated: ${months[date.getMonth()]} ${date.getDate()} ${date.getFullYear()}`;

    card_text.append(questions, updated);
    body.append(title, card_text);
    card.append(image, body);
    col.append(card);

    return col;
}

// display requested category questions
function get_questions(id) {
    console.log(id);
    const main = document.querySelector('main');
    fetch(`/api/category/${id}`)
    .then(response => response.json())
    .then(result => {
        fetch(`/user/info/`)
        .then(_response => _response.json())
        .then(user => {
            main.innerText = null;
            const questions = document.createElement('div');
            setId(questions, 'questions');
            questions.classList.add('row', 'g-3', 'p-3', 'mx-auto');
            const h1 = document.createElement('h1');
            h1.classList.add('text-center');
            h1.innerText = result.name;
            if (user.is_admin) {
                var form = document.querySelector('#questionForm');
                const addQuestionBtn = `<div class="float-end btn-group"><a data-bs-toggle="collapse" href="#questionForm" role="button" aria-expanded="false" aria-controls="collapseExample" class="btn btn-outline-primary" title="Add question"><svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/></svg></a></div>`;
                h1.innerHTML += addQuestionBtn;
            }
            questions.append(h1, form);
            main.append(questions);
        });
    });
}

function load_navbar() {
    fetch('/user/info/')
    .then(response => response.json())
    .then(user => {
        const nav = document.querySelector('nav');
        nav.classList.add('navbar', 'navbar-expand-lg', 'bg-secondary', 'sticky-top');

        const container = document.createElement('div');
        container.classList.add('container-fluid');

        const brand = document.createElement('a');
        brand.classList.add('navbar-brand');
        brand.setAttribute('href', '/');
        brand.innerHTML = '<img src="static/Test/images/logo.png" class="img-fluid" width="50px" height="50px">';

        const toggler = document.createElement('button');
        toggler.classList.add('navbar-toggler', 'me-2');
        toggler.setAttribute('type', 'button');
        setDataAttribute(toggler, 'toggle', 'collapse');
        toggler.innerHTML = '<span class="navbar-toggler-icon"></span>';

        const div = document.createElement('div');
        div.classList.add('collapse', 'navbar-collapse');
        setId(div, 'navbarSupportedContent');

        const ul = document.createElement('ul');
        ul.classList.add('navbar-nav', 'me-auto', 'mb-2', 'mb-lg-0')

        const home = create_tab(['nav-item'], ['nav-link'], 'home', '');
        const search = create_tab(['nav-item'], ['nav-link'], 'search', 'search');
        ul.append(home, search);

        const logout = create_tab(['nav-item'], ['nav-link'], 'logout', 'accounts/logout');
        ul.append(logout);

        if (user.is_admin) {
            const dropdown = document.createElement('li');
            dropdown.classList.add('nav-item', 'dropdown');

            const link = document.createElement('a');
            link.innerText = 'More';
            link.classList.add('nav-link', 'dropdown-toggle');
            link.setAttribute('href', '#');
            setId(link, 'navbarDropdown');
            link.setAttribute('role', 'button');
            setDataAttribute(link, 'toggle', 'dropdown');
            link.setAttribute('aria-expanded', 'false');

            const dropdown_ul = document.createElement('ul');
            dropdown_ul.classList.add('dropdown-menu');
            dropdown_ul.setAttribute('aria-labelledby', 'navbarDropdown');

            const add_category = create_tab([], ['dropdown-item'], 'Add Category');
            const add_question = create_tab([], ['dropdown-item'], 'Add Question', 'add/question');
            const add_questions = create_tab([], [], '');
            add_questions.innerHTML = '<button type="button" class="dropdown-item" data-bs-toggle="modal" data-bs-target="#exampleModal" data-bs-whatever="@mdo">Upload Questions</button>';
            const divider = create_tab([], [], '');
            divider.innerHTML = '<hr class="dropdown-divider">';
            const admin = create_tab([], ['dropdown-item'], 'Admin Panel', 'admin/');


            dropdown_ul.append(add_category, add_question, add_questions, divider, admin);
            dropdown.append(link, dropdown_ul);
            ul.append(dropdown);
        }

        // profile image
        const profile = document.createElement('div');
        profile.classList.add('ms-auto', 'me-1');
        profile.innerHTML = '<div class="d-flex">\
        <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="text-white bi bi-person-circle" viewBox="0 0 16 16">\
        <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>\
        <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>\
        </svg>\
        </div>';

        div.append(ul)
        container.append(brand, div, profile, toggler);
        nav.append(container);
    });
}

/*
create navbar tab
- arg1 expects array of classes for li
- arg2 expects array of classes for a tag
- arg3 expects
*/
function create_tab(li_classes, tab_classes, txt, href='#') {
    const li = document.createElement('li');    // create navbar item
    const tab = document.createElement('a');    // create a tag
    tab.setAttribute('id', `${txt.toLowerCase()}`);
    tab.setAttribute('href', href);
    if (typeof(li_classes) === 'object' && typeof(tab_classes) === 'object'){
        // add css classes to li
        for (let cls in li_classes) {
            li.classList.add(li_classes[cls]);
        }
        // add css classes to tag
        for (let cls in tab_classes) {
            tab.classList.add(tab_classes[cls]);
        }
    }
    tab.innerText = txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase();; // set text
    li.append(tab)
    return li;
}

// load header
function load_header() {
    const header = document.querySelector('#header');
    header.classList.add('text-center', 'display-6');
    header.innerText = 'Test Your Skills and Enhance your memory';
}

// set data attribute of an element
function setDataAttribute(t, e, i) {
    t.setAttribute(`data-bs-${e}`, i);
}

// set id
function setId(t, i) {
    t.setAttribute('id', i);
}

// set element t style e to i
function setStyle(t, e, i) {
    t.style[e] = i;
}
