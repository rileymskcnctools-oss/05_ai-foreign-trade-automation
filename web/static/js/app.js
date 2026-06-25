/* FT Workspace v3.0 — 全局 JS */
function showToast(msg, type='success') {
    const t = document.createElement('div');
    t.className = `fixed top-4 right-4 px-4 py-2 rounded-lg text-white text-sm z-50 shadow-lg ${type==='success'?'bg-green-500':type==='error'?'bg-red-500':'bg-blue-500'}`;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}
async function copyToClipboard(text) {
    try { await navigator.clipboard.writeText(text); showToast('已复制到剪贴板'); }
    catch(e) { showToast('复制失败','error'); }
}
function formatNumber(n) { return new Intl.NumberFormat().format(n); }
function formatCurrency(a) { return new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(a); }
