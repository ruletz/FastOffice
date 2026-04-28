import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

script = """
<style id="nuclear-style-v2">
/* HIDE TOP HEADER STRUCTURALLY */
.main-header, .box-header, #box-header, .top-panel {
    display: none !important;
    height: 0px !important;
    min-height: 0px !important;
    max-height: 0px !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* RECAPTURE SPACE */
.main-panel, #mainpnl, .app-body, .viewport {
    top: 40px !important;
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* LOGOS */
.logo-text, .title-text, .app-name, #idx-about-appname, #idx-about-version, .box-copyright, span[class*='logo-text'] {
    display: none !important;
    opacity: 0 !important;
}
.box-ver .ver-logo, .left-panel-logo, .logo {
    max-width: 32px !important;
    width: 32px !important;
    overflow: hidden !important;
    display: block !important;
}
.box-ver {
    max-width: 32px !important;
}

/* CLOUD BUTTONS - Left/Right Panels */
.btn-clouds, #idx-btn-clouds, #right-menu-clouds, button[id*='cloud'], .left-menu-clouds, li[id*='cloud'], li[data-id*='cloud'], a[href*='cloud'] {
    display: none !important;
}

/* TABS BAR FLEX LAYOUT (For saving tools migration) */
.toolbar-tabs-container, .toolbar-tabs-wrapper {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
}
.toolbar-tabs-container ul, .toolbar-tabs {
    display: flex !important;
    align-items: center !important;
    margin: 0 !important;
    padding: 0 !important;
}
.custom-header-tools {
    display: flex !important;
    align-items: center !important;
    padding: 0 15px !important;
    height: 100% !important;
}
.custom-header-title {
    display: flex !important;
    align-items: center !important;
    padding: 0 15px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    max-width: 300px !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    text-overflow: ellipsis !important;
    height: 100% !important;
}
</style>

<script id="nuclear_ui_v2">
document.addEventListener("DOMContentLoaded", function() {
    var toolsMoved = false;

    setInterval(function() {
        
        // --- HIDE TABS BY TEXT ---
        var allTabs = document.querySelectorAll("li, .tab, .x-tab");
        for (var i = 0; i < allTabs.length; i++) {
            var el = allTabs[i];
            var txt = (el.innerText || el.textContent || "").toLowerCase().trim();
            if (txt.indexOf("collaboration") !== -1 || 
                txt.indexOf("plugin") !== -1 || 
                txt.indexOf("protection") !== -1 ||
                txt.indexOf("ai") === 0) {
                el.style.display = "none";
            }
        }
        
        // --- HIDE BUTTONS BY TEXT ---
        var buttons = document.querySelectorAll("button, .btn, .x-btn, .menu-item, a, .btn-text, span, div.button");
        for (var b = 0; b < buttons.length; b++) {
            var elBtn = buttons[b];
            var bTxt = (elBtn.innerText || elBtn.textContent || "").toLowerCase().trim();
            var idTxt = (elBtn.id || "").toLowerCase();
            
            if (bTxt === "editing" || 
                bTxt === "reviewing" || 
                bTxt === "viewing" ||
                bTxt.indexOf("cloud") !== -1 || 
                bTxt === "onlyoffice" ||
                idTxt.indexOf("cloud") !== -1 ||
                idTxt.indexOf("mode") !== -1) {
                
                elBtn.style.display = "none";
                
                var parentLi = elBtn.closest('li') || elBtn.closest('.menu-item');
                if (parentLi) {
                    parentLi.style.display = "none";
                }
            }
        }

        // --- FIX TOP-LEFT LOGO TEXT ---
        var logos = document.querySelectorAll('.logo-text, .title-text, .app-name, [class*="logo-text"]');
        for (var l = 0; l < logos.length; l++) {
            logos[l].style.display = "none";
            logos[l].innerHTML = "";
        }
        
        var leftLogoBoxes = document.querySelectorAll('.box-ver .ver-logo, .left-panel-logo, .logo');
        for (var lb = 0; lb < leftLogoBoxes.length; lb++) {
            leftLogoBoxes[lb].style.width = "32px";
            leftLogoBoxes[lb].style.maxWidth = "32px";
            leftLogoBoxes[lb].style.overflow = "hidden";
        }

        // --- MIGRATE ICONS & TITLE ---
        var tabsUl = document.querySelector(".toolbar-tabs-container ul") || document.querySelector(".toolbar-tabs");
        var tools = document.querySelector(".header-tools") || document.querySelector(".header-left") || document.querySelector("#box-header .left-panel");
        var titleBox = document.querySelector(".header-title") || document.querySelector("#document-title");

        if (tabsUl && tools && titleBox) {
            
            tools.classList.add("custom-header-tools");
            titleBox.classList.add("custom-header-title");
            
            tools.style.display = "flex";
            titleBox.style.display = "flex";

            if (!toolsMoved) {
                var viewNode = null;
                for (var t = 0; t < allTabs.length; t++) {
                    var cText = (allTabs[t].innerText || allTabs[t].textContent || "").toLowerCase().trim();
                    if (cText === "view" || cText === "exibir" || cText === "ver") { 
                        viewNode = allTabs[t].closest('li'); 
                        if (!viewNode) viewNode = allTabs[t];
                        break;
                    }
                }

                if (viewNode && viewNode.parentNode === tabsUl && viewNode.nextSibling) {
                    tabsUl.insertBefore(tools, viewNode.nextSibling);
                    tabsUl.insertBefore(titleBox, tools.nextSibling);
                } else {
                    tabsUl.appendChild(tools);
                    tabsUl.appendChild(titleBox);
                }
                toolsMoved = true;
            }
        }

        // --- MURDER THE TOP BAR ---
        var topBars = document.querySelectorAll(".box-header, .main-header, #box-header, .top-panel");
        for (var tb = 0; tb < topBars.length; tb++) {
            if (topBars[tb].classList.contains('main-panel') || topBars[tb].id === 'mainpnl') continue;
            
            if (toolsMoved) {
                topBars[tb].style.display = "none";
                topBars[tb].style.height = "0px";
                topBars[tb].style.visibility = "hidden";
            }
        }
        
    }, 100);
});
</script>
"""

text = re.sub(r'<style id="nuclear-style.*?">.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<script id="nuclear_ui.*?">.*?</script>', '', text, flags=re.DOTALL)
text = text.replace('</head>', script + '\n</head>')

with codecs.open(html_path, 'w', 'utf8') as f:
    f.write(text)

print("index.html patched heavily.")
