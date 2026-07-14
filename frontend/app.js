/* ~~~ UserPost 98 engine room ~~~
   100% certified vanilla JavaScript, just like grandma used to write */

var API = "http://localhost:8000";

/* ---------- tiny api helper: adds the Bearer token, screams on errors ---------- */
async function api(path, options) {
    options = options || {};
    options.headers = options.headers || {};
    if (options.body) options.headers["Content-Type"] = "application/json";
    var token = localStorage.getItem("token");
    if (token) options.headers["Authorization"] = "Bearer " + token;

    var res = await fetch(API + path, options);
    if (res.status === 401) {
        localStorage.removeItem("token");
        refreshLoginBar();
        showSection("home");
        throw new Error("Yer session expired or yer not logged in!! Log in again, cyber-surfer.");
    }
    if (!res.ok) {
        var detail = "Something went kaput (HTTP " + res.status + ")";
        try { detail = (await res.json()).detail || detail; } catch (e) {}
        throw new Error(detail);
    }
    if (res.status === 204) return null;
    return res.json();
}

function esc(s) {
    var d = document.createElement("div");
    d.appendChild(document.createTextNode(s == null ? "" : String(s)));
    return d.innerHTML;
}

function retroDate(iso) {
    var d = new Date(iso);
    return d.toLocaleDateString() + " @ " + d.toLocaleTimeString();
}

/* ---------- sections ---------- */
function showSection(name) {
    var sections = ["home", "forgot", "guestbook", "members", "mypage"];
    for (var i = 0; i < sections.length; i++) {
        var el = document.getElementById("section-" + sections[i]);
        if (el) el.style.display = (sections[i] === name) ? "" : "none";
    }
    if (name === "guestbook") loadGuestbook();
    if (name === "members") loadMembers();
    if (name === "mypage") loadMyPage();
}

function refreshLoginBar() {
    var el = document.getElementById("login-status-blink");
    if (localStorage.getItem("token")) {
        el.innerHTML = "&#9989; YOU ARE LOGGED IN AND TOTALLY RADICAL &#9989;";
        el.style.color = "#008000";
    } else {
        el.innerHTML = "&#9210; YOU ARE NOT LOGGED IN &#9210;";
        el.style.color = "#FF0000";
    }
}

/* ---------- auth ---------- */
async function register() {
    try {
        var user = await api("/auth/register", {
            method: "POST",
            body: JSON.stringify({
                username: document.getElementById("reg-username").value,
                email: document.getElementById("reg-email").value,
                password: document.getElementById("reg-password").value
            })
        });
        alert("WELCOME TO THE CREW, " + user.username + "!!!\nNow log in with yer email + password.");
    } catch (e) { alert("REGISTRATION FAILED!!\n" + e.message); }
}

async function login() {
    try {
        var data = await api("/auth/login", {
            method: "POST",
            body: JSON.stringify({
                email: document.getElementById("login-email").value,
                password: document.getElementById("login-password").value
            })
        });
        localStorage.setItem("token", data.access_token);
        refreshLoginBar();
        alert("ACCESS GRANTED!! Welcome back to cyberspace.");
        showSection("guestbook");
    } catch (e) { alert("ACCESS DENIED!!\n" + e.message); }
}

function logout() {
    localStorage.removeItem("token");
    refreshLoginBar();
    alert("You have left cyberspace. Come back soon!!");
    showSection("home");
}

async function forgotPassword() {
    try {
        var data = await api("/auth/forgot-password", {
            method: "POST",
            body: JSON.stringify({ email: document.getElementById("forgot-email").value })
        });
        alert(data.message + "\n\n(Go peek at the server log for the secret code!)");
    } catch (e) { alert("OOPS!!\n" + e.message); }
}

async function changePassword() {
    try {
        await api("/auth/change-password", {
            method: "POST",
            body: JSON.stringify({
                email: document.getElementById("reset-email").value,
                security_code: document.getElementById("reset-code").value,
                new_password: document.getElementById("reset-password").value
            })
        });
        alert("PASSWORD CHANGED!! You are a security wizard now. Go log in!");
        showSection("home");
    } catch (e) { alert("NO DICE!!\n" + e.message); }
}

/* ---------- guestbook (posts) ---------- */
async function loadGuestbook() {
    var box = document.getElementById("guestbook-entries");
    try {
        var posts = await api("/users/get_posts");
        if (!posts.length) {
            box.innerHTML = "<center><font face='Comic Sans MS'>Nobody signed yet... be the FIRST!! &#127942;</font></center>";
            return;
        }
        posts.sort(function (a, b) { return new Date(b.created_at) - new Date(a.created_at); });
        var html = "";
        for (var i = 0; i < posts.length; i++) {
            var p = posts[i];
            html += "<div class='gb-entry'>" +
                "<span class='gb-head'>&#128100; " + esc(p.username) + " wuz here ~ " + retroDate(p.created_at) + "</span>" +
                "<hr>" + esc(p.content) + "</div>";
        }
        box.innerHTML = html;
    } catch (e) {
        box.innerHTML = "<center><font color='red'>" + esc(e.message) + "</font></center>";
    }
}

async function signGuestbook() {
    var content = document.getElementById("post-content").value;
    if (!content.trim()) { alert("Write something first, silly!!"); return; }
    try {
        await api("/users/post", { method: "POST", body: JSON.stringify({ content: content }) });
        document.getElementById("post-content").value = "";
        loadGuestbook();
    } catch (e) { alert("SIGNING FAILED!!\n" + e.message); }
}

/* ---------- members ---------- */
async function loadMembers() {
    var box = document.getElementById("members-list");
    try {
        var users = await api("/users/");
        var html = "<table width='100%' border='2' cellpadding='6' cellspacing='0' class='bevel-out' bgcolor='#C0C0C0'>" +
            "<tr bgcolor='#000080'>" +
            "<td><font color='#FFFF00'><b>#</b></font></td>" +
            "<td><font color='#FFFF00'><b>USERNAME</b></font></td>" +
            "<td><font color='#FFFF00'><b>E-MAIL</b></font></td>" +
            "<td><font color='#FFFF00'><b>CYBER-CITIZEN SINCE</b></font></td></tr>";
        for (var i = 0; i < users.length; i++) {
            var u = users[i];
            html += "<tr class='member-row' bgcolor='" + (i % 2 ? "#FFFFFF" : "#FFFFCC") + "'>" +
                "<td>" + u.id + "</td>" +
                "<td><b>" + esc(u.username) + "</b></td>" +
                "<td>" + esc(u.email) + "</td>" +
                "<td>" + retroDate(u.created_at) + "</td></tr>";
        }
        box.innerHTML = html + "</table>";
    } catch (e) {
        box.innerHTML = "<center><font color='red'>" + esc(e.message) + "</font></center>";
    }
}

/* ---------- my page ---------- */
async function loadMyPage() {
    var info = document.getElementById("my-info");
    var postsBox = document.getElementById("my-posts");
    try {
        var me = await api("/users/current");
        info.innerHTML = "<center><table border='2' cellpadding='8' class='bevel-out' bgcolor='#FFFFCC'><tr><td>" +
            "<font face='Courier New'>" +
            "<b>USERNAME:</b> " + esc(me.username) + "<br>" +
            "<b>E-MAIL:</b> " + esc(me.email) + "<br>" +
            "<b>MEMBER SINCE:</b> " + retroDate(me.created_at) + "<br>" +
            "<b>LAST UPDATED:</b> " + retroDate(me.updated) +
            "</font></td></tr></table></center>";

        var posts = await api("/users/get_my_posts");
        if (!posts.length) {
            postsBox.innerHTML = "<center><font face='Comic Sans MS'>You haven't signed the guestbook yet!! What are you waiting for??</font></center>";
            return;
        }
        var html = "";
        for (var i = 0; i < posts.length; i++) {
            html += "<div class='gb-entry'>" +
                "<span class='gb-head'>" + retroDate(posts[i].created_at) + "</span>" +
                "<hr>" + esc(posts[i].content) + "</div>";
        }
        postsBox.innerHTML = html;
    } catch (e) {
        info.innerHTML = "<center><font color='red'>" + esc(e.message) + "</font></center>";
        postsBox.innerHTML = "";
    }
}

/* ---------- world-famous fake hit counter ---------- */
function bumpHitCounter() {
    var hits = parseInt(localStorage.getItem("hits") || "31337", 10) + 1;
    localStorage.setItem("hits", String(hits));
    document.getElementById("hit-counter").textContent = String(hits).padStart(6, "0");
}

/* ---------- boot ---------- */
bumpHitCounter();
refreshLoginBar();
showSection(localStorage.getItem("token") ? "guestbook" : "home");
