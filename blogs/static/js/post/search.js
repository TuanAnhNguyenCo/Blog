hide_content = document.getElementsByClassName("hide-content");
search = document.getElementById("search");
search_form = document.getElementById("search-form");
function showContent()
{
    for(let i=0;i<hide_content.length;i++)
        hide_content[i].style.display = "block";
    
    search.style.display = "none";
}
function showSearchPage()
{
    for(let i=0;i<hide_content.length;i++)
        hide_content[i].style.display = "none";
    search.style.display = "block";
    
}
