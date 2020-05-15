for (var i = 0; i < 16; i++) {
    const x = document.getElementsByClassName("box")[i];
    const y = document.getElementsByClassName("image")[i];
    const z = document.getElementsByClassName("hover_box")[i];
    const w = document.getElementsByClassName("hover_text")[i];
    const n = document.getElementsByTagName("a")[i];
    x.addEventListener("mouseenter", function () {
        y.style.opacity = 0.6;
        z.style.opacity = 1;
        w.style.opacity = 1;
    });
    x.addEventListener("mouseleave", function () {
        y.style.opacity = 1;
        z.style.opacity = 0;
        w.style.opacity = 0;
    });
    n.addEventListener("click", function (e) {
        var myModal = document.getElementById("big_modal");

        myModal.style.display = "block";
        var myImg = document.getElementById("modal_image");
        myImg.src = e.currentTarget.firstElementChild.src;
        e.preventDefault();
    });
}
const m = document.getElementById("big_modal");
m.addEventListener("click", function(e){
    console.log(e.target.id)
    if (e.target.id == "big_modal"){
        var myModal = document.getElementById("big_modal");
        myModal.style.display = "none";
    }
});