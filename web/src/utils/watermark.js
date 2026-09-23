/**
 * 创建系统水印
 * @param {string} username - 登录用户名
 */
export function createSecureWatermark(username) {
  // 1. 若已存在水印则先移除
  const oldWatermark = document.querySelector('.system-watermark');
  if (oldWatermark) document.body.removeChild(oldWatermark);

  // 2. 创建水印容器
  const watermark = document.createElement('div');
  watermark.className = 'system-watermark';

  // 3. 生成水印SVG
  const svgStr = `
    <svg xmlns="http://www.w3.org/2000/svg" width="600" height="300">
      <text x="50%" y="50%"
        font-size="20"
        fill="rgba(180,180,180,0.2)"
        text-anchor="middle"
        transform="rotate(-20, 150, 75)">
        ${username} ${new Date().toLocaleDateString()}
      </text>
    </svg>
  `;

  // 4. 设置水印样式
  Object.assign(watermark.style, {
    position: 'fixed',
    top: '95px',
    left: '0',
    width: '100%',
    height: '100%',
    pointerEvents: 'none',
    backgroundImage: `url("data:image/svg+xml;utf8,${encodeURIComponent(svgStr)}")`,
    backgroundRepeat: 'repeat',
    zIndex: '9999'
  });

  // 5. 防删除保护（监听DOM变化自动恢复水印）
  const observer = new MutationObserver(() => {
    if (!document.body.contains(watermark)) {
      document.body.appendChild(watermark);
    }
  });
  observer.observe(document.body, { childList: true });

  // 6. 添加到页面
  document.body.appendChild(watermark);

  // 返回清除方法
  return () => {
    observer.disconnect();
    watermark.remove();
  };
}
