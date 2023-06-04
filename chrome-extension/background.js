chrome.browserAction.onClicked.addListener(function (tab) {
    chrome.tabs.create({
      url: 'http://chrome.soumit.in:5000',
      selected: true,
    })
})