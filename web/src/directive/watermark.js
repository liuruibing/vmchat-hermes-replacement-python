import Vue from 'vue';
export default () => {
	Vue.directive('watermark', (el, binding) => {
	    function addWaterMarker(str1, str2, parentNode, font, textColor) { // str1、str2水印文字，父元素，字体，文字颜色
	    	var img = document.createElement('canvas'); // 创建canvas元素
			parentNode.appendChild(img);
			img.width = 240;
			img.height = 150;
			img.style.display = 'none';
			var imgs = img.getContext('2d'); // 获取canvas画布
			imgs.rotate(-20 * Math.PI / 180); // 逆时针旋转π/9
			imgs.font = font || '16px Microsoft JhengHei';
			imgs.fillStyle = textColor || 'rgba(200, 200, 200, 0.3)';
			imgs.textAlign = 'left';
			imgs.textBaseline = 'Middle';
			imgs.fillText(str1, 15, 80); // 第一行字体
			imgs.fillText(str2, 15, 100); // 第二行字体
			parentNode.style.backgroundImage = 'url(' + img.toDataURL('image/png') + ')';
	    }
	    addWaterMarker(binding.value.text1, binding.value.text2, el, binding.value.font, binding.value.textColor);
	})
}