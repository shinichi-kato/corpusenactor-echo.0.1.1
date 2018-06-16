// ajaxchat.js - AJAXでチャットアプリ風のUIを実装します。

// 親スクリプトで設定されるパラメータ
MAIN_LOG_DISPLAY_LEN = MAIN_LOG_DISPLAY_LEN || 10

// チャット画面は常に最下行までスクロールされた状態にする。
// これにより最新の行を見るのにスクロールが不要になるとともに、iOSなどでキーボードを表示させた
// 時にキーボードと重ならないようにチャット画面がスクロールされる。
(function() {
  var timer = 0;
  window.onresize = function() {
    if (timer>0){ clearTimeout(timer);}
    timer = setTimeout(function(){
      window.scrollTo(0,document.body.scrollHeight);
    }, 200);
  };
}());

function createBalloon(node)
{
  var side = node.side  || 'left'
  var speech = node.speech  || 'error'

  var e = document.createElement('div')
  e.setAttribute('class','balloon '+side+'-box')
  e.innerHTML=
    '<div class="balloonbox">'+
    '<div id="balloon-'+side+'">'+
    '<p class="txt">'+speech+'</p></div></div>'+
    '<p class="img"><img src="static/'+side+'.png"/></p>'

  return e
}

function AjaxRequest(command)
{
  var r = new XMLHttpRequest()
  r.onreadystatechange = function()
  {
    if(r.readyState == 4) // 非同期
    {
      if(r.status == 200) // OKが返ってきた
      {
        var j = JSON.parse(r.responseText)
        var w = document.getElementById('mainwindow')
        for (let n of j.log){
          w.appendChild(createBalloon(n))
        }
        while (w.childElementCount > MAIN_LOG_DISPLAY_LEN){
          w.removeChild(w.firstChild)
        }
      }
    }
  }
  r.open('POST','/ajax')
  r.setRequestHeader("Content-type","application/json")
  var speech = document.getElementById('speech').value
  if (command == null) command = ''
  r.send(JSON.stringify({'command':command,'speech':speech}))
}

function engage()
{
  AjaxRequest()
  var s = document.getElementById('speech')
  var n = {
    'side':'right',
    'speech':s.value
  }
  document.getElementById('mainwindow').appendChild(createBalloon(n))
  s.value = ""
  window.scrollTo(0,document.body.scrollHeight);
  return false /*false を返すとhtmlをリロードしない*/
}
