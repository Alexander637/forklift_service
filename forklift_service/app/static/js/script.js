function showTab(tabName) {
    var tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(function(tab) {
        tab.style.display = 'none';
    });

    var activeTab = document.getElementById(tabName);
    if (activeTab) {
        activeTab.style.display = 'block';
    }
}
