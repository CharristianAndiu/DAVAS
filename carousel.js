//轮播图切换
let currentIndex = 0;
const slides = document.querySelectorAll(".slide");
const slideContainer = document.querySelector(".slide-container");

function showSlide(index) {
    if (index < 0) {
        currentIndex = slides.length - 1;
    } else if (index >= slides.length) {
        currentIndex = 0;
    }

    slideContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
}

function prevSlide() {
    currentIndex--;
    showSlide(currentIndex);
}

function nextSlide() {
    currentIndex++;
    showSlide(currentIndex);
}

// 初始显示第一张图片
showSlide(currentIndex);