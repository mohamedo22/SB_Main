window.addEventListener('scroll', function() {
    if (window.scrollY > 5) {
        document.querySelector("header").style.backgroundColor = "black";
        document.querySelectorAll(".nav-items").forEach(function(item) {
            item.style.color = "white";
        });
    } else {
        document.querySelector("header").style.backgroundColor = "";
        document.querySelectorAll(".nav-items").forEach(function(item) {
            item.style.color = "";
        });
    }
});
let el = 0;
function NextElement(elementNumber)
{
    let userRemoveActive = document.getElementById(`user${el+1}`);
    userRemoveActive.classList.remove('activeUser');
    el++;
    console.log(el);
    if(el > 4)
    {
        el=0;
    }
    let userAddActive = document.getElementById(`user${el+1}`);
    userAddActive.classList.add('activeUser');
    if(window.innerWidth >= 1000)
    {
            document.querySelector(`.wrapper${elementNumber}`).style.marginLeft = `${-el*34}rem`;
    }
    else
    {
        document.querySelector(`.wrapper${elementNumber}`).style.marginLeft = `${-el*33.5}rem`;
    }
    document.querySelectorAll(`.thempn${elementNumber}`).forEach((el)=>
    {
        el.style.backgroundColor = 'silver';
    });
    document.querySelector(`.ThembNav${el}${elementNumber}`).style.backgroundColor = 'black';
}
function LastElement(elementNumber)
{
    el--;
    console.log(el);
    if(el < 0)
    {
        el=4;
    }
    if(window.innerWidth >= 1000)
        {
                document.querySelector(`.wrapper${elementNumber}`).style.marginLeft = `${-el*25}rem`;
        }
        else
        {
            document.querySelector(`.wrapper${elementNumber}`).style.marginLeft = `${-el*26}rem`;
        }
    document.querySelectorAll(`.thempn${elementNumber}`).forEach((el)=>
        {
            el.style.backgroundColor = 'silver';
        });
        document.querySelector(`.ThembNav${el}${elementNumber}`).style.backgroundColor = 'black';
}
document.querySelectorAll(".ContainerOFinksFooter:not(.formContainer)").forEach((el) => {
    el.addEventListener("click", function() {
        let height = el.style.height;
        if (height === '1rem') {
            el.style.height = 'max-content';
        } else {
            el.style.height = '1rem';
        }
    });
});


