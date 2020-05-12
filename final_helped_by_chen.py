import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
import time
import os
from important_info import important_info

def testFinal():
    source = '''<html  dir="ltr" lang="zh-cn" xml:lang="zh-cn">
<head>
    <title>形考作业1  (15分）</title>
    <link rel="shortcut icon" href="http://hubei.ouchn.cn/theme/image.php/blueonionres/theme/1587093656/favicon" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="keywords" content="moodle, 形考作业1  (15分）" />
<link rel="stylesheet" type="text/css" href="http://hubei.ouchn.cn/theme/yui_combo.php?rollup/3.17.2/yui-moodlesimple-min.css" /><script id="firstthemesheet" type="text/css">/** Required in order to fix style inclusion problems in IE with YUI **/</script><link rel="stylesheet" type="text/css" href="http://hubei.ouchn.cn/theme/styles.php/blueonionres/1587093656/all" />
<script type="text/javascript">
//<![CDATA[
var M = {}; M.yui = {};
M.pageloadstarttime = new Date();
M.cfg = {"wwwroot":"http:\/\/hubei.ouchn.cn","sesskey":"UjZLOQhC3W","themerev":"1587093656","slasharguments":1,"theme":"blueonionres","iconsystemmodule":"core\/icon_system_fontawesome","jsrev":-1,"admin":"admin","svgicons":true,"usertimezone":"\u4e9a\u6d32\/\u4e0a\u6d77","contextid":964046};var yui1ConfigFn = function(me) {if(/-skin|reset|fonts|grids|base/.test(me.name)){me.type='css';me.path=me.path.replace(/\.js/,'.css');me.path=me.path.replace(/\/yui2-skin/,'/assets/skins/sam/yui2-skin')}};
var yui2ConfigFn = function(me) {var parts=me.name.replace(/^moodle-/,'').split('-'),component=parts.shift(),module=parts[0],min='-min';if(/-(skin|core)$/.test(me.name)){parts.pop();me.type='css';min=''}
if(module){var filename=parts.join('-');me.path=component+'/'+module+'/'+filename+min+'.'+me.type}else{me.path=component+'/'+component+'.'+me.type}};
YUI_config = {"debug":false,"base":"http:\/\/hubei.ouchn.cn\/lib\/yuilib\/3.17.2\/","comboBase":"http:\/\/hubei.ouchn.cn\/theme\/yui_combo.php?","combine":true,"filter":null,"insertBefore":"firstthemesheet","groups":{"yui2":{"base":"http:\/\/hubei.ouchn.cn\/lib\/yuilib\/2in3\/2.9.0\/build\/","comboBase":"http:\/\/hubei.ouchn.cn\/theme\/yui_combo.php?","combine":true,"ext":false,"root":"2in3\/2.9.0\/build\/","patterns":{"yui2-":{"group":"yui2","configFn":yui1ConfigFn}}},"moodle":{"name":"moodle","base":"http:\/\/hubei.ouchn.cn\/theme\/yui_combo.php?m\/-1\/","combine":true,"comboBase":"http:\/\/hubei.ouchn.cn\/theme\/yui_combo.php?","ext":false,"root":"m\/-1\/","patterns":{"moodle-":{"group":"moodle","configFn":yui2ConfigFn}},"filter":null,"modules":{"moodle-core-actionmenu":{"requires":["base","event","node-event-simulate"]},"moodle-core-event":{"requires":["event-custom"]},"moodle-core-handlebars":{"condition":{"trigger":"handlebars","when":"after"}},"moodle-core-formchangechecker":{"requires":["base","event-focus","moodle-core-event"]},"moodle-core-dragdrop":{"requires":["base","node","io","dom","dd","event-key","event-focus","moodle-core-notification"]},"moodle-core-blocks":{"requires":["base","node","io","dom","dd","dd-scroll","moodle-core-dragdrop","moodle-core-notification"]},"moodle-core-notification":{"requires":["moodle-core-notification-dialogue","moodle-core-notification-alert","moodle-core-notification-confirm","moodle-core-notification-exception","moodle-core-notification-ajaxexception"]},"moodle-core-notification-dialogue":{"requires":["base","node","panel","escape","event-key","dd-plugin","moodle-core-widget-focusafterclose","moodle-core-lockscroll"]},"moodle-core-notification-alert":{"requires":["moodle-core-notification-dialogue"]},"moodle-core-notification-confirm":{"requires":["moodle-core-notification-dialogue"]},"moodle-core-notification-exception":{"requires":["moodle-core-notification-dialogue"]},"moodle-core-notification-ajaxexception":{"requires":["moodle-core-notification-dialogue"]},"moodle-core-tooltip":{"requires":["base","node","io-base","moodle-core-notification-dialogue","json-parse","widget-position","widget-position-align","event-outside","cache-base"]},"moodle-core-dock":{"requires":["base","node","event-custom","event-mouseenter","event-resize","escape","moodle-core-dock-loader","moodle-core-event"]},"moodle-core-dock-loader":{"requires":["escape"]},"moodle-core-chooserdialogue":{"requires":["base","panel","moodle-core-notification"]},"moodle-core-checknet":{"requires":["base-base","moodle-core-notification-alert","io-base"]},"moodle-core-lockscroll":{"requires":["plugin","base-build"]},"moodle-core-languninstallconfirm":{"requires":["base","node","moodle-core-notification-confirm","moodle-core-notification-alert"]},"moodle-core-maintenancemodetimer":{"requires":["base","node"]},"moodle-core-popuphelp":{"requires":["moodle-core-tooltip"]},"moodle-core_availability-form":{"requires":["base","node","event","event-delegate","panel","moodle-core-notification-dialogue","json"]},"moodle-backup-backupselectall":{"requires":["node","event","node-event-simulate","anim"]},"moodle-backup-confirmcancel":{"requires":["node","node-event-simulate","moodle-core-notification-confirm"]},"moodle-course-modchooser":{"requires":["moodle-core-chooserdialogue","moodle-course-coursebase"]},"moodle-course-categoryexpander":{"requires":["node","event-key"]},"moodle-course-dragdrop":{"requires":["base","node","io","dom","dd","dd-scroll","moodle-core-dragdrop","moodle-core-notification","moodle-course-coursebase","moodle-course-util"]},"moodle-course-util":{"requires":["node"],"use":["moodle-course-util-base"],"submodules":{"moodle-course-util-base":{},"moodle-course-util-section":{"requires":["node","moodle-course-util-base"]},"moodle-course-util-cm":{"requires":["node","moodle-course-util-base"]}}},"moodle-course-formatchooser":{"requires":["base","node","node-event-simulate"]},"moodle-course-management":{"requires":["base","node","io-base","moodle-core-notification-exception","json-parse","dd-constrain","dd-proxy","dd-drop","dd-delegate","node-event-delegate"]},"moodle-form-showadvanced":{"requires":["node","base","selector-css3"]},"moodle-form-dateselector":{"requires":["base","node","overlay","calendar"]},"moodle-form-passwordunmask":{"requires":[]},"moodle-form-shortforms":{"requires":["node","base","selector-css3","moodle-core-event"]},"moodle-question-searchform":{"requires":["base","node"]},"moodle-question-chooser":{"requires":["moodle-core-chooserdialogue"]},"moodle-question-preview":{"requires":["base","dom","event-delegate","event-key","core_question_engine"]},"moodle-question-qbankmanager":{"requires":["node","selector-css3"]},"moodle-availability_completion-form":{"requires":["base","node","event","moodle-core_availability-form"]},"moodle-availability_date-form":{"requires":["base","node","event","io","moodle-core_availability-form"]},"moodle-availability_grade-form":{"requires":["base","node","event","moodle-core_availability-form"]},"moodle-availability_group-form":{"requires":["base","node","event","moodle-core_availability-form"]},"moodle-availability_grouping-form":{"requires":["base","node","event","moodle-core_availability-form"]},"moodle-availability_profile-form":{"requires":["base","node","event","moodle-core_availability-form"]},"moodle-qtype_ddimageortext-form":{"requires":["moodle-qtype_ddimageortext-dd","form_filepicker"]},"moodle-qtype_ddimageortext-dd":{"requires":["node","dd","dd-drop","dd-constrain"]},"moodle-qtype_ddmarker-form":{"requires":["moodle-qtype_ddmarker-dd","form_filepicker","graphics","escape"]},"moodle-qtype_ddmarker-dd":{"requires":["node","event-resize","dd","dd-drop","dd-constrain","graphics"]},"moodle-qtype_ddwtos-dd":{"requires":["node","dd","dd-drop","dd-constrain"]},"moodle-mod_assign-history":{"requires":["node","transition"]},"moodle-mod_bigbluebuttonbn-modform":{"requires":["base","node"]},"moodle-mod_bigbluebuttonbn-broker":{"requires":["base","node","datasource-get","datasource-jsonschema","datasource-polling","moodle-core-notification"]},"moodle-mod_bigbluebuttonbn-imports":{"requires":["base","node"]},"moodle-mod_bigbluebuttonbn-recordings":{"requires":["base","node","datasource-get","datasource-jsonschema","datasource-polling","moodle-core-notification"]},"moodle-mod_bigbluebuttonbn-rooms":{"requires":["base","node","datasource-get","datasource-jsonschema","datasource-polling","moodle-core-notification"]},"moodle-mod_forum-subscriptiontoggle":{"requires":["base-base","io-base"]},"moodle-mod_quiz-questionchooser":{"requires":["moodle-core-chooserdialogue","moodle-mod_quiz-util","querystring-parse"]},"moodle-mod_quiz-modform":{"requires":["base","node","event"]},"moodle-mod_quiz-dragdrop":{"requires":["base","node","io","dom","dd","dd-scroll","moodle-core-dragdrop","moodle-core-notification","moodle-mod_quiz-quizbase","moodle-mod_quiz-util-base","moodle-mod_quiz-util-page","moodle-mod_quiz-util-slot","moodle-course-util"]},"moodle-mod_quiz-randomquestion":{"requires":["base","event","node","io","moodle-core-notification-dialogue"]},"moodle-mod_quiz-util":{"requires":["node","moodle-core-actionmenu"],"use":["moodle-mod_quiz-util-base"],"submodules":{"moodle-mod_quiz-util-base":{},"moodle-mod_quiz-util-slot":{"requires":["node","moodle-mod_quiz-util-base"]},"moodle-mod_quiz-util-page":{"requires":["node","moodle-mod_quiz-util-base"]}}},"moodle-mod_quiz-toolboxes":{"requires":["base","node","event","event-key","io","moodle-mod_quiz-quizbase","moodle-mod_quiz-util-slot","moodle-core-notification-ajaxexception"]},"moodle-mod_quiz-quizquestionbank":{"requires":["base","event","node","io","io-form","yui-later","moodle-question-qbankmanager","moodle-core-notification-dialogue"]},"moodle-mod_quiz-autosave":{"requires":["base","node","event","event-valuechange","node-event-delegate","io-form"]},"moodle-mod_quiz-repaginate":{"requires":["base","event","node","io","moodle-core-notification-dialogue"]},"moodle-mod_quiz-quizbase":{"requires":["base","node"]},"moodle-mod_videofile-videojs":{"requires":["base","node","event"]},"moodle-message_airnotifier-toolboxes":{"requires":["base","node","io"]},"moodle-filter_glossary-autolinker":{"requires":["base","node","io-base","json-parse","event-delegate","overlay","moodle-core-event","moodle-core-notification-alert","moodle-core-notification-exception","moodle-core-notification-ajaxexception"]},"moodle-filter_mathjaxloader-loader":{"requires":["moodle-core-event"]},"moodle-editor_atto-rangy":{"requires":[]},"moodle-editor_atto-editor":{"requires":["node","transition","io","overlay","escape","event","event-simulate","event-custom","node-event-html5","node-event-simulate","yui-throttle","moodle-core-notification-dialogue","moodle-core-notification-confirm","moodle-editor_atto-rangy","handlebars","timers","querystring-stringify"]},"moodle-editor_atto-plugin":{"requires":["node","base","escape","event","event-outside","handlebars","event-custom","timers","moodle-editor_atto-menu"]},"moodle-editor_atto-menu":{"requires":["moodle-core-notification-dialogue","node","event","event-custom"]},"moodle-format_grid-gridkeys":{"requires":["event-nav-keys"]},"moodle-report_eventlist-eventfilter":{"requires":["base","event","node","node-event-delegate","datatable","autocomplete","autocomplete-filters"]},"moodle-report_loglive-fetchlogs":{"requires":["base","event","node","io","node-event-delegate"]},"moodle-gradereport_grader-gradereporttable":{"requires":["base","node","event","handlebars","overlay","event-hover"]},"moodle-gradereport_history-userselector":{"requires":["escape","event-delegate","event-key","handlebars","io-base","json-parse","moodle-core-notification-dialogue"]},"moodle-tool_capability-search":{"requires":["base","node"]},"moodle-tool_lp-dragdrop-reorder":{"requires":["moodle-core-dragdrop"]},"moodle-tool_monitor-dropdown":{"requires":["base","event","node"]},"moodle-assignfeedback_editpdf-editor":{"requires":["base","event","node","io","graphics","json","event-move","event-resize","transition","querystring-stringify-simple","moodle-core-notification-dialog","moodle-core-notification-alert","moodle-core-notification-exception","moodle-core-notification-ajaxexception"]},"moodle-atto_accessibilitychecker-button":{"requires":["color-base","moodle-editor_atto-plugin"]},"moodle-atto_accessibilityhelper-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_align-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_bold-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_charmap-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_clear-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_collapse-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_emoticon-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_equation-button":{"requires":["moodle-editor_atto-plugin","moodle-core-event","io","event-valuechange","tabview","array-extras"]},"moodle-atto_html-button":{"requires":["moodle-editor_atto-plugin","event-valuechange"]},"moodle-atto_image-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_indent-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_italic-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_link-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_managefiles-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_managefiles-usedfiles":{"requires":["node","escape"]},"moodle-atto_media-button":{"requires":["moodle-editor_atto-plugin","moodle-form-shortforms"]},"moodle-atto_noautolink-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_orderedlist-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_rtl-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_strike-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_subscript-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_superscript-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_table-button":{"requires":["moodle-editor_atto-plugin","moodle-editor_atto-menu","event","event-valuechange"]},"moodle-atto_title-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_underline-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_undo-button":{"requires":["moodle-editor_atto-plugin"]},"moodle-atto_unorderedlist-button":{"requires":["moodle-editor_atto-plugin"]}}},"gallery":{"name":"gallery","base":"http:\/\/hubei.ouchn.cn\/lib\/yuilib\/gallery\/","combine":true,"comboBase":"http:\/\/hubei.ouchn.cn\/theme\/yui_combo.php?","ext":false,"root":"gallery\/-1\/","patterns":{"gallery-":{"group":"gallery"}}}},"modules":{"core_filepicker":{"name":"core_filepicker","fullpath":"http:\/\/hubei.ouchn.cn\/lib\/javascript.php\/-1\/repository\/filepicker.js","requires":["base","node","node-event-simulate","json","async-queue","io-base","io-upload-iframe","io-form","yui2-treeview","panel","cookie","datatable","datatable-sort","resize-plugin","dd-plugin","escape","moodle-core_filepicker","moodle-core-notification-dialogue"]},"core_comment":{"name":"core_comment","fullpath":"http:\/\/hubei.ouchn.cn\/lib\/javascript.php\/-1\/comment\/comment.js","requires":["base","io-base","node","json","yui2-animation","overlay","escape"]},"mathjax":{"name":"mathjax","fullpath":"https:\/\/cdnjs.cloudflare.com\/ajax\/libs\/mathjax\/2.7.1\/MathJax.js?delayStartupUntil=configured"},"core_question_flags":{"name":"core_question_flags","fullpath":"http:\/\/hubei.ouchn.cn\/lib\/javascript.php\/-1\/question\/flags.js","requires":["base","dom","event-delegate","io-base"]},"core_question_engine":{"name":"core_question_engine","fullpath":"http:\/\/hubei.ouchn.cn\/lib\/javascript.php\/-1\/question\/qengine.js","requires":["node","event"]},"mod_quiz":{"name":"mod_quiz","fullpath":"http:\/\/hubei.ouchn.cn\/lib\/javascript.php\/-1\/mod\/quiz\/module.js","requires":["base","dom","event-delegate","event-key","core_question_engine","moodle-core-formchangechecker"]}}};
M.yui.loader = {modules: {}};

//]]>
</script>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body  id="page-mod-quiz-attempt" class="format-flexsections  path-mod path-mod-quiz safari dir-ltr lang-zh_cn yui-skin-sam yui3-skin-sam hubei-ouchn-cn pagelayout-incourse course-5284 context-964046 cmid-659661 category-13 ">

<div id="page-wrapper" style="margin-bottom:-75px;padding-bottom:0">

    <div>
    <a class="sr-only sr-only-focusable" href="#maincontent">跳到主要内容</a>
</div><script type="text/javascript" src="http://hubei.ouchn.cn/theme/yui_combo.php?rollup/3.17.2/yui-moodlesimple-min.js"></script><script type="text/javascript" src="http://hubei.ouchn.cn/lib/javascript.php/-1/lib/javascript-static.js"></script>
<script type="text/javascript">
//<![CDATA[
document.body.className += ' jsenabled';
//]]>
</script>



    <header style="position:relative" role="banner" class="pos-f-t navbar navbar-full navbar-light bg-faded navbar-static-top moodle-has-zindex">
    
        <div class="container-fluid navbar-nav">
    
            <div data-region="drawer-toggle">
           
              
                 <button onClick=" $('.link').slideToggle() " type="button" class="btn pull-xs-left m-r-1 btn-secondary" ><i class="icon fa fa-bars fa-fw " aria-hidden="true"  aria-label=""></i><span class="sr-only">停靠面板</span></button>
    
             
    
            </div>
    <!--网站全名及其logo的显示-->
    <!-- 以前的原码
            <a  href="http://hubei.ouchn.cn" class="navbar-brand 
                    hidden-sm-down
                    ">
                  <span class="site-name hidden-sm-down">湖北</span>
            </a>
    
    -->
    
    <a  style="display:inline-block;margin-top:-5px;"  href = "http://hubei.ouchn.cn" class="navbar-brand has-logo
    
        ">
    <!--logo不存在时在检查网站的logo并输出他-->
    
             
                  <img class="logo" src="http://hubei.ouchn.cn/theme/image.php/blueonionres/theme/1587093656/logo" alt="湖北">
              
    
    
            <!-- custom_navigation自定义的链接 -->
            
                <a class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/course/view.php?id=5284 " title="课程首页">课程首页</a>
              
                <a style='margin-left:20px'  class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/course/view.php?id=5284&test=1" title="形考汇集">形考任务</a>
                
                
               
                <a style='margin-left:20px'  class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/mod/page/view.php?id=659504&j=1" title="教学团队">教学团队</a><a style='margin-left:20px'  class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/course/view.php?id=5284&forum=1" title="学习论坛">学习论坛</a>
    
            <!-- navbar_plugin_output 显示通知和消息 -->
            
            <!-- user_menu -->
            <div class="usermenu"><div class="action-menu moodle-actionmenu nowrap-items" id="action-menu-1" data-enhance="moodle-core-actionmenu">

        <div class="menubar" id="action-menu-1-menubar" role="menubar">

            <div class="dropdown d-inline">
    <a href="#" class="dropdown-toggle" id="dropdown-1" title="" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="userbutton"><span class="avatars"><span class="avatar current"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/u/f2" alt="吴蔓的头像" title="吴蔓的头像" class="userpicture defaultuserpic" width="35" height="35" role="presentation" /></span></span></span><b class="caret"></b></a>
        <div class="dropdown-menu dropdown-menu-right menu  align-tr-br" id="action-menu-1-menu" data-rel="menu-content" aria-labelledby="action-menu-toggle-1" role="menu" data-align="tr-br">
            <a href="http://hubei.ouchn.cn/my/" class="dropdown-item menu-action" role="menuitem"data-title="mymoodle,admin" aria-labelledby="actionmenuaction-1"><i class="icon fa fa-tachometer fa-fw " aria-hidden="true" title="个人主页" aria-label="个人主页"></i><span class="menu-action-text" id="actionmenuaction-1">个人主页</span></a><div class="dropdown-divider"></div><a href="http://hubei.ouchn.cn/user/profile.php?id=135249" class="dropdown-item menu-action" role="menuitem"data-title="profile,moodle" aria-labelledby="actionmenuaction-2"><i class="icon fa fa-user fa-fw " aria-hidden="true" title="个人档案" aria-label="个人档案"></i><span class="menu-action-text" id="actionmenuaction-2">个人档案</span></a><a href="http://hubei.ouchn.cn/grade/report/overview/index.php" class="dropdown-item menu-action" role="menuitem"data-title="grades,grades" aria-labelledby="actionmenuaction-3"><i class="icon fa fa-table fa-fw " aria-hidden="true" title="成绩" aria-label="成绩"></i><span class="menu-action-text" id="actionmenuaction-3">成绩</span></a><a href="http://hubei.ouchn.cn/message/index.php" class="dropdown-item menu-action" role="menuitem"data-title="messages,message" aria-labelledby="actionmenuaction-4"><i class="icon fa fa-comment fa-fw " aria-hidden="true" title="消息" aria-label="消息"></i><span class="menu-action-text" id="actionmenuaction-4">消息</span></a><a href="http://hubei.ouchn.cn/user/preferences.php" class="dropdown-item menu-action" role="menuitem"data-title="preferences,moodle" aria-labelledby="actionmenuaction-5"><i class="icon fa fa-wrench fa-fw " aria-hidden="true" title="使用偏好" aria-label="使用偏好"></i><span class="menu-action-text" id="actionmenuaction-5">使用偏好</span></a><div class="dropdown-divider"></div><a href="http://hubei.ouchn.cn/login/logout.php?sesskey=UjZLOQhC3W" class="dropdown-item menu-action" role="menuitem"data-title="logout,moodle" aria-labelledby="actionmenuaction-6"><i class="icon fa fa-sign-out fa-fw " aria-hidden="true" title="退出" aria-label="退出"></i><span class="menu-action-text" id="actionmenuaction-6">退出</span></a>
        </div>
</div>


        </div>

</div></div>
            <!-- search_box -->
            <span class="hidden-md-down">
            
            </span>
     
    
        </div>
    
    </header>
    
    
        <div class="link">
         
                 
                <a class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/course/view.php?id=5284 " title="课程首页">课程首页</a>
              
                <a style='margin-left:20px'  class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/course/view.php?id=5284&test=1" title="形考汇集">形考任务</a>
                
                
               
                <a style='margin-left:20px'  class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/mod/page/view.php?id=659504&j=1" title="教学团队">教学团队</a><a style='margin-left:20px'  class="nav-item nav-link header_link" href="http://hubei.ouchn.cn/course/view.php?id=5284&forum=1" title="学习论坛">学习论坛</a>
            
        </div>
    <div id="page" class="container-fluid">
        <div class="pull-xs-right context-header-settings-menu"></div><div class="breadcrumb-button pull-xs-right"></div>

        <div id="page-content" class="row">
            <div id="region-main-box" class="col-xs-12">
                <section id="region-main" style="border:none;max-width:1200px;margin:0 auto;float:none" class="has-blocks">
                    <div class="card card-block">
                    <div role="main"><span id="maincontent"></span><form action="http://hubei.ouchn.cn/mod/quiz/processattempt.php" method="post" enctype="multipart/form-data" accept-charset="utf-8" id="responseform"><div><div id="q1" class="que description informationitem notyetanswered"><div class="info"><div class="state"></div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:1_:flagged" value="0" /><input type="checkbox" id="q6826251:1_:flaggedcheckbox" name="q6826251:1_:flagged" value="1" /><input type="hidden" value="qaid=112217873&amp;qubaid=6826251&amp;qid=1605753&amp;slot=1&amp;checksum=f901724aafa665179bcf29adbeaf7069&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:1_:flaggedlabel" for="q6826251:1_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:1_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">信息文本</h4><input type="hidden" name="q6826251:1_:sequencecheck" value="1" /><div class="qtext"><p>一、单选题（每题3分，共60分）</p></div><div class="im-controls"><input type="hidden" name="q6826251:1_-seen" value="1" /></div></div></div></div><div id="q2" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">1</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:2_:flagged" value="0" /><input type="checkbox" id="q6826251:2_:flaggedcheckbox" name="q6826251:2_:flagged" value="1" /><input type="hidden" value="qaid=112217874&amp;qubaid=6826251&amp;qid=1605754&amp;slot=2&amp;checksum=5e650d736391e43c03bb847ba538bb99&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:2_:flaggedlabel" for="q6826251:2_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:2_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:2_:sequencecheck" value="1" /><div class="qtext"><p>在P2P网络中，节点的功能不包括（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:2_answer" value="0" id="q6826251:2_answer0" /><label for="q6826251:2_answer0" class="m-l-1">A. 下载</label> </div>
<div class="r1"><input type="radio" name="q6826251:2_answer" value="1" id="q6826251:2_answer1" /><label for="q6826251:2_answer1" class="m-l-1">B. 生成</label> </div>
<div class="r0"><input type="radio" name="q6826251:2_answer" value="2" id="q6826251:2_answer2" /><label for="q6826251:2_answer2" class="m-l-1">C. 加密</label> </div>
<div class="r1"><input type="radio" name="q6826251:2_answer" value="3" id="q6826251:2_answer3" /><label for="q6826251:2_answer3" class="m-l-1">D. 信息追踪</label> </div>
</div></div></div></div></div><div id="q3" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">2</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:3_:flagged" value="0" /><input type="checkbox" id="q6826251:3_:flaggedcheckbox" name="q6826251:3_:flagged" value="1" /><input type="hidden" value="qaid=112217875&amp;qubaid=6826251&amp;qid=1605755&amp;slot=3&amp;checksum=c52b7352fbeb333df6a459f3ebceb7ed&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:3_:flaggedlabel" for="q6826251:3_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:3_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:3_:sequencecheck" value="1" /><div class="qtext"><p>关于WWW服务，下列说法中错误的是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:3_answer" value="0" id="q6826251:3_answer0" /><label for="q6826251:3_answer0" class="m-l-1">A. 可显示多媒体信息</label> </div>
<div class="r1"><input type="radio" name="q6826251:3_answer" value="1" id="q6826251:3_answer1" /><label for="q6826251:3_answer1" class="m-l-1">B. 使用超链接技术</label> </div>
<div class="r0"><input type="radio" name="q6826251:3_answer" value="2" id="q6826251:3_answer2" /><label for="q6826251:3_answer2" class="m-l-1">C. 工作在客户端/服务器模式</label> </div>
<div class="r1"><input type="radio" name="q6826251:3_answer" value="3" id="q6826251:3_answer3" /><label for="q6826251:3_answer3" class="m-l-1">D. 用于提供高速文件传输服务</label> </div>
</div></div></div></div></div><div id="q4" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">3</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:4_:flagged" value="0" /><input type="checkbox" id="q6826251:4_:flaggedcheckbox" name="q6826251:4_:flagged" value="1" /><input type="hidden" value="qaid=112217876&amp;qubaid=6826251&amp;qid=1605756&amp;slot=4&amp;checksum=c6ba1deb572fc6f814e0feb14ab85339&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:4_:flaggedlabel" for="q6826251:4_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:4_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:4_:sequencecheck" value="1" /><div class="qtext"><p>（ ）不属于计算机网络四要素。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:4_answer" value="0" id="q6826251:4_answer0" /><label for="q6826251:4_answer0" class="m-l-1">A. 计算机系统</label> </div>
<div class="r1"><input type="radio" name="q6826251:4_answer" value="1" id="q6826251:4_answer1" /><label for="q6826251:4_answer1" class="m-l-1">B. 用户</label> </div>
<div class="r0"><input type="radio" name="q6826251:4_answer" value="2" id="q6826251:4_answer2" /><label for="q6826251:4_answer2" class="m-l-1">C. 传输介质</label> </div>
<div class="r1"><input type="radio" name="q6826251:4_answer" value="3" id="q6826251:4_answer3" /><label for="q6826251:4_answer3" class="m-l-1">D. 网络协议</label> </div>
</div></div></div></div></div><div id="q5" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">4</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:5_:flagged" value="0" /><input type="checkbox" id="q6826251:5_:flaggedcheckbox" name="q6826251:5_:flagged" value="1" /><input type="hidden" value="qaid=112217877&amp;qubaid=6826251&amp;qid=1605757&amp;slot=5&amp;checksum=00a24bd55547c13b0d88f84f7234ad72&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:5_:flaggedlabel" for="q6826251:5_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:5_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:5_:sequencecheck" value="1" /><div class="qtext"><p>计算机网络的基本功能包括（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:5_answer" value="0" id="q6826251:5_answer0" /><label for="q6826251:5_answer0" class="m-l-1">A. 数据处理、信号分析</label> </div>
<div class="r1"><input type="radio" name="q6826251:5_answer" value="1" id="q6826251:5_answer1" /><label for="q6826251:5_answer1" class="m-l-1">B. 数据存储、资源管理</label> </div>
<div class="r0"><input type="radio" name="q6826251:5_answer" value="2" id="q6826251:5_answer2" /><label for="q6826251:5_answer2" class="m-l-1">C. 数据传输、资源共享</label> </div>
<div class="r1"><input type="radio" name="q6826251:5_answer" value="3" id="q6826251:5_answer3" /><label for="q6826251:5_answer3" class="m-l-1">D. 任务调度、设备管理</label> </div>
</div></div></div></div></div><div id="q6" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">5</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:6_:flagged" value="0" /><input type="checkbox" id="q6826251:6_:flaggedcheckbox" name="q6826251:6_:flagged" value="1" /><input type="hidden" value="qaid=112217878&amp;qubaid=6826251&amp;qid=1605758&amp;slot=6&amp;checksum=8ddab52e496f7d12402a4a4029d538f8&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:6_:flaggedlabel" for="q6826251:6_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:6_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:6_:sequencecheck" value="1" /><div class="qtext"><p>计算机网络中广域网和局域网的分类是以（ ）来划分的。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:6_answer" value="0" id="q6826251:6_answer0" /><label for="q6826251:6_answer0" class="m-l-1">A. 信息交换方式</label> </div>
<div class="r1"><input type="radio" name="q6826251:6_answer" value="1" id="q6826251:6_answer1" /><label for="q6826251:6_answer1" class="m-l-1">B. 传输控制方法</label> </div>
<div class="r0"><input type="radio" name="q6826251:6_answer" value="2" id="q6826251:6_answer2" /><label for="q6826251:6_answer2" class="m-l-1">C. 网络使用习惯</label> </div>
<div class="r1"><input type="radio" name="q6826251:6_answer" value="3" id="q6826251:6_answer3" /><label for="q6826251:6_answer3" class="m-l-1">D. 网络覆盖范围</label> </div>
</div></div></div></div></div><div id="q7" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">6</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:7_:flagged" value="0" /><input type="checkbox" id="q6826251:7_:flaggedcheckbox" name="q6826251:7_:flagged" value="1" /><input type="hidden" value="qaid=112217879&amp;qubaid=6826251&amp;qid=1605759&amp;slot=7&amp;checksum=41ebad7bdcbc266b8b1b3e71f2d25e33&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:7_:flaggedlabel" for="q6826251:7_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:7_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:7_:sequencecheck" value="1" /><div class="qtext"><p>（ ）网络结构简单、灵活，可扩充性好，传输速率高，响应速度快。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:7_answer" value="0" id="q6826251:7_answer0" /><label for="q6826251:7_answer0" class="m-l-1">A. 总线型</label> </div>
<div class="r1"><input type="radio" name="q6826251:7_answer" value="1" id="q6826251:7_answer1" /><label for="q6826251:7_answer1" class="m-l-1">B. 星型</label> </div>
<div class="r0"><input type="radio" name="q6826251:7_answer" value="2" id="q6826251:7_answer2" /><label for="q6826251:7_answer2" class="m-l-1">C. 树型</label> </div>
<div class="r1"><input type="radio" name="q6826251:7_answer" value="3" id="q6826251:7_answer3" /><label for="q6826251:7_answer3" class="m-l-1">D. 环型</label> </div>
</div></div></div></div></div><div id="q8" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">7</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:8_:flagged" value="0" /><input type="checkbox" id="q6826251:8_:flaggedcheckbox" name="q6826251:8_:flagged" value="1" /><input type="hidden" value="qaid=112217880&amp;qubaid=6826251&amp;qid=1605760&amp;slot=8&amp;checksum=6dadb95f08afe08a89707680df6a08d8&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:8_:flaggedlabel" for="q6826251:8_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:8_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:8_:sequencecheck" value="1" /><div class="qtext"><p>（ ）属于分组交换的特点。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:8_answer" value="0" id="q6826251:8_answer0" /><label for="q6826251:8_answer0" class="m-l-1">A. 建立连接的时间长</label> </div>
<div class="r1"><input type="radio" name="q6826251:8_answer" value="1" id="q6826251:8_answer1" /><label for="q6826251:8_answer1" class="m-l-1">B. 报文大小不一</label> </div>
<div class="r0"><input type="radio" name="q6826251:8_answer" value="2" id="q6826251:8_answer2" /><label for="q6826251:8_answer2" class="m-l-1">C. 数据传输前不需要建立一条端到端的通路</label> </div>
<div class="r1"><input type="radio" name="q6826251:8_answer" value="3" id="q6826251:8_answer3" /><label for="q6826251:8_answer3" class="m-l-1">D. 出错后整个报文全部重发</label> </div>
</div></div></div></div></div><div id="q9" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">8</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:9_:flagged" value="0" /><input type="checkbox" id="q6826251:9_:flaggedcheckbox" name="q6826251:9_:flagged" value="1" /><input type="hidden" value="qaid=112217881&amp;qubaid=6826251&amp;qid=1605761&amp;slot=9&amp;checksum=99eb7edd299ec8448499f38916b7167b&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:9_:flaggedlabel" for="q6826251:9_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:9_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:9_:sequencecheck" value="1" /><div class="qtext"><p>计算机网络协议的三要素为（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:9_answer" value="0" id="q6826251:9_answer0" /><label for="q6826251:9_answer0" class="m-l-1">A. 语法、语义和同步</label> </div>
<div class="r1"><input type="radio" name="q6826251:9_answer" value="1" id="q6826251:9_answer1" /><label for="q6826251:9_answer1" class="m-l-1">B. 语法、语义和规程</label> </div>
<div class="r0"><input type="radio" name="q6826251:9_answer" value="2" id="q6826251:9_answer2" /><label for="q6826251:9_answer2" class="m-l-1">C. 语法、功能和同步</label> </div>
<div class="r1"><input type="radio" name="q6826251:9_answer" value="3" id="q6826251:9_answer3" /><label for="q6826251:9_answer3" class="m-l-1">D. 语法、同步和规程</label> </div>
</div></div></div></div></div><div id="q10" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">9</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:10_:flagged" value="0" /><input type="checkbox" id="q6826251:10_:flaggedcheckbox" name="q6826251:10_:flagged" value="1" /><input type="hidden" value="qaid=112217882&amp;qubaid=6826251&amp;qid=1605762&amp;slot=10&amp;checksum=5788eb637746388af5fdefa9f82e8dd2&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:10_:flaggedlabel" for="q6826251:10_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:10_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:10_:sequencecheck" value="1" /><div class="qtext"><p>开放系统互联参考模型OSI/RM的最底层是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:10_answer" value="0" id="q6826251:10_answer0" /><label for="q6826251:10_answer0" class="m-l-1">A. 物理层</label> </div>
<div class="r1"><input type="radio" name="q6826251:10_answer" value="1" id="q6826251:10_answer1" /><label for="q6826251:10_answer1" class="m-l-1">B. 网络层</label> </div>
<div class="r0"><input type="radio" name="q6826251:10_answer" value="2" id="q6826251:10_answer2" /><label for="q6826251:10_answer2" class="m-l-1">C. 传输层</label> </div>
<div class="r1"><input type="radio" name="q6826251:10_answer" value="3" id="q6826251:10_answer3" /><label for="q6826251:10_answer3" class="m-l-1">D. 应用层</label> </div>
</div></div></div></div></div><div id="q11" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">10</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:11_:flagged" value="0" /><input type="checkbox" id="q6826251:11_:flaggedcheckbox" name="q6826251:11_:flagged" value="1" /><input type="hidden" value="qaid=112217883&amp;qubaid=6826251&amp;qid=1605763&amp;slot=11&amp;checksum=2272121666fdbb6de422359000dbd058&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:11_:flaggedlabel" for="q6826251:11_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:11_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:11_:sequencecheck" value="1" /><div class="qtext"><p>在TCP/IP协议体系中，将网络结构自上而下划分为四层：（1）应用层；（2）传输层；（3）网际层；（4）网络接口层。工作时，（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:11_answer" value="0" id="q6826251:11_answer0" /><label for="q6826251:11_answer0" class="m-l-1">A. 发送方从下层向上层传输数据，每经过一层附加协议控制信息</label> </div>
<div class="r1"><input type="radio" name="q6826251:11_answer" value="1" id="q6826251:11_answer1" /><label for="q6826251:11_answer1" class="m-l-1">B. 接收方从下层向上层传输数据，每经过一层附加协议控制信息</label> </div>
<div class="r0"><input type="radio" name="q6826251:11_answer" value="2" id="q6826251:11_answer2" /><label for="q6826251:11_answer2" class="m-l-1">C. 发送方从上层向下层传输数据，每经过一层附加协议控制信息</label> </div>
<div class="r1"><input type="radio" name="q6826251:11_answer" value="3" id="q6826251:11_answer3" /><label for="q6826251:11_answer3" class="m-l-1">D. 接收方从上层向下层传输数据，每经过一层附加协议控制信息</label> </div>
</div></div></div></div></div><div id="q12" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">11</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:12_:flagged" value="0" /><input type="checkbox" id="q6826251:12_:flaggedcheckbox" name="q6826251:12_:flagged" value="1" /><input type="hidden" value="qaid=112217884&amp;qubaid=6826251&amp;qid=1605764&amp;slot=12&amp;checksum=dc61ace0033d0dacc55e251436c3590a&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:12_:flaggedlabel" for="q6826251:12_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:12_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:12_:sequencecheck" value="1" /><div class="qtext"><p>下列属于TCP/IP模型中网际层协议的是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:12_answer" value="0" id="q6826251:12_answer0" /><label for="q6826251:12_answer0" class="m-l-1">A. FTP</label> </div>
<div class="r1"><input type="radio" name="q6826251:12_answer" value="1" id="q6826251:12_answer1" /><label for="q6826251:12_answer1" class="m-l-1">B. HTTP</label> </div>
<div class="r0"><input type="radio" name="q6826251:12_answer" value="2" id="q6826251:12_answer2" /><label for="q6826251:12_answer2" class="m-l-1">C. DNS</label> </div>
<div class="r1"><input type="radio" name="q6826251:12_answer" value="3" id="q6826251:12_answer3" /><label for="q6826251:12_answer3" class="m-l-1">D. ICMP</label> </div>
</div></div></div></div></div><div id="q13" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">12</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:13_:flagged" value="0" /><input type="checkbox" id="q6826251:13_:flaggedcheckbox" name="q6826251:13_:flagged" value="1" /><input type="hidden" value="qaid=112217885&amp;qubaid=6826251&amp;qid=1605765&amp;slot=13&amp;checksum=9d0f8d208afbf6c4bc01d7a9b3dee455&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:13_:flaggedlabel" for="q6826251:13_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:13_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:13_:sequencecheck" value="1" /><div class="qtext"><p>下列属于TCP/IP模型中应用层协议的是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:13_answer" value="0" id="q6826251:13_answer0" /><label for="q6826251:13_answer0" class="m-l-1">A. ARP</label> </div>
<div class="r1"><input type="radio" name="q6826251:13_answer" value="1" id="q6826251:13_answer1" /><label for="q6826251:13_answer1" class="m-l-1">B. RARP</label> </div>
<div class="r0"><input type="radio" name="q6826251:13_answer" value="2" id="q6826251:13_answer2" /><label for="q6826251:13_answer2" class="m-l-1">C. SMTP</label> </div>
<div class="r1"><input type="radio" name="q6826251:13_answer" value="3" id="q6826251:13_answer3" /><label for="q6826251:13_answer3" class="m-l-1">D. ICMP</label> </div>
</div></div></div></div></div><div id="q14" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">13</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:14_:flagged" value="0" /><input type="checkbox" id="q6826251:14_:flaggedcheckbox" name="q6826251:14_:flagged" value="1" /><input type="hidden" value="qaid=112217886&amp;qubaid=6826251&amp;qid=1605766&amp;slot=14&amp;checksum=1eda8a2ac9576cd832eccc3880a1ae92&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:14_:flaggedlabel" for="q6826251:14_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:14_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:14_:sequencecheck" value="1" /><div class="qtext"><p>IEEE802委员会定义的快速以太网的协议标准是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:14_answer" value="0" id="q6826251:14_answer0" /><label for="q6826251:14_answer0" class="m-l-1">A. IEEE802.2z</label> </div>
<div class="r1"><input type="radio" name="q6826251:14_answer" value="1" id="q6826251:14_answer1" /><label for="q6826251:14_answer1" class="m-l-1">B. IEEE802.3</label> </div>
<div class="r0"><input type="radio" name="q6826251:14_answer" value="2" id="q6826251:14_answer2" /><label for="q6826251:14_answer2" class="m-l-1">C. IEEE802.3a</label> </div>
<div class="r1"><input type="radio" name="q6826251:14_answer" value="3" id="q6826251:14_answer3" /><label for="q6826251:14_answer3" class="m-l-1">D. IEEE802.3u</label> </div>
</div></div></div></div></div><div id="q15" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">14</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:15_:flagged" value="0" /><input type="checkbox" id="q6826251:15_:flaggedcheckbox" name="q6826251:15_:flagged" value="1" /><input type="hidden" value="qaid=112217887&amp;qubaid=6826251&amp;qid=1605767&amp;slot=15&amp;checksum=dcf68f44c4c369775f98eb8e31ae76cb&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:15_:flaggedlabel" for="q6826251:15_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:15_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:15_:sequencecheck" value="1" /><div class="qtext"><p>下列以太网（ ）使用双绞线作为传输介质。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:15_answer" value="0" id="q6826251:15_answer0" /><label for="q6826251:15_answer0" class="m-l-1">A. 10Base2</label> </div>
<div class="r1"><input type="radio" name="q6826251:15_answer" value="1" id="q6826251:15_answer1" /><label for="q6826251:15_answer1" class="m-l-1">B. 10Base5</label> </div>
<div class="r0"><input type="radio" name="q6826251:15_answer" value="2" id="q6826251:15_answer2" /><label for="q6826251:15_answer2" class="m-l-1">C. 10BaseT</label> </div>
<div class="r1"><input type="radio" name="q6826251:15_answer" value="3" id="q6826251:15_answer3" /><label for="q6826251:15_answer3" class="m-l-1">D. 1000BASE-LX</label> </div>
</div></div></div></div></div><div id="q16" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">15</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:16_:flagged" value="0" /><input type="checkbox" id="q6826251:16_:flaggedcheckbox" name="q6826251:16_:flagged" value="1" /><input type="hidden" value="qaid=112217888&amp;qubaid=6826251&amp;qid=1605768&amp;slot=16&amp;checksum=3932b86166c1f07a6c4cad271082be30&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:16_:flaggedlabel" for="q6826251:16_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:16_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:16_:sequencecheck" value="1" /><div class="qtext"><p>局域网的典型特性是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:16_answer" value="0" id="q6826251:16_answer0" /><label for="q6826251:16_answer0" class="m-l-1">A. 高数据速率，大范围，高误码率</label> </div>
<div class="r1"><input type="radio" name="q6826251:16_answer" value="1" id="q6826251:16_answer1" /><label for="q6826251:16_answer1" class="m-l-1">B. 低数据速率，小范围，低误码率</label> </div>
<div class="r0"><input type="radio" name="q6826251:16_answer" value="2" id="q6826251:16_answer2" /><label for="q6826251:16_answer2" class="m-l-1">C. 高数据速率，小范围，低误码率</label> </div>
<div class="r1"><input type="radio" name="q6826251:16_answer" value="3" id="q6826251:16_answer3" /><label for="q6826251:16_answer3" class="m-l-1">D. 低数据速率，小范围，高误码率</label> </div>
</div></div></div></div></div><div id="q17" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">16</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:17_:flagged" value="0" /><input type="checkbox" id="q6826251:17_:flaggedcheckbox" name="q6826251:17_:flagged" value="1" /><input type="hidden" value="qaid=112217889&amp;qubaid=6826251&amp;qid=1605769&amp;slot=17&amp;checksum=a91b1e0b62c71d905a14ce0d45d8b239&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:17_:flaggedlabel" for="q6826251:17_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:17_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:17_:sequencecheck" value="1" /><div class="qtext"><p>对局域网的特点描述错误的是（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:17_answer" value="0" id="q6826251:17_answer0" /><label for="q6826251:17_answer0" class="m-l-1">A. 传输速率高，通常为10～100Mbps</label> </div>
<div class="r1"><input type="radio" name="q6826251:17_answer" value="1" id="q6826251:17_answer1" /><label for="q6826251:17_answer1" class="m-l-1">B. 支持多种传输介质</label> </div>
<div class="r0"><input type="radio" name="q6826251:17_answer" value="2" id="q6826251:17_answer2" /><label for="q6826251:17_answer2" class="m-l-1">C. 传输质量好，误码率低</label> </div>
<div class="r1"><input type="radio" name="q6826251:17_answer" value="3" id="q6826251:17_answer3" /><label for="q6826251:17_answer3" class="m-l-1">D. 无规则的拓扑结构</label> </div>
</div></div></div></div></div><div id="q18" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">17</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:18_:flagged" value="0" /><input type="checkbox" id="q6826251:18_:flaggedcheckbox" name="q6826251:18_:flagged" value="1" /><input type="hidden" value="qaid=112217890&amp;qubaid=6826251&amp;qid=1605770&amp;slot=18&amp;checksum=5dc9d1261995d38fc7f7c0c44c85551d&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:18_:flaggedlabel" for="q6826251:18_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:18_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:18_:sequencecheck" value="1" /><div class="qtext"><p>交换机工作在OSI七层模型中的（ ）层。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:18_answer" value="0" id="q6826251:18_answer0" /><label for="q6826251:18_answer0" class="m-l-1">A. 物理层</label> </div>
<div class="r1"><input type="radio" name="q6826251:18_answer" value="1" id="q6826251:18_answer1" /><label for="q6826251:18_answer1" class="m-l-1">B. 数据链路层</label> </div>
<div class="r0"><input type="radio" name="q6826251:18_answer" value="2" id="q6826251:18_answer2" /><label for="q6826251:18_answer2" class="m-l-1">C. 网络层</label> </div>
<div class="r1"><input type="radio" name="q6826251:18_answer" value="3" id="q6826251:18_answer3" /><label for="q6826251:18_answer3" class="m-l-1">D. 应用层</label> </div>
</div></div></div></div></div><div id="q19" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">18</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:19_:flagged" value="0" /><input type="checkbox" id="q6826251:19_:flaggedcheckbox" name="q6826251:19_:flagged" value="1" /><input type="hidden" value="qaid=112217891&amp;qubaid=6826251&amp;qid=1605771&amp;slot=19&amp;checksum=a38f977fae950ed58c0c986f5c73bc10&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:19_:flaggedlabel" for="q6826251:19_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:19_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:19_:sequencecheck" value="1" /><div class="qtext"><p>（ ）是一种居民宽带接入网，在原有有线电视网的基础上发展而来。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:19_answer" value="0" id="q6826251:19_answer0" /><label for="q6826251:19_answer0" class="m-l-1">A. 光纤同轴混合网（HFC）</label> </div>
<div class="r1"><input type="radio" name="q6826251:19_answer" value="1" id="q6826251:19_answer1" /><label for="q6826251:19_answer1" class="m-l-1">B. 高速数字用户线（HDSL）</label> </div>
<div class="r0"><input type="radio" name="q6826251:19_answer" value="2" id="q6826251:19_answer2" /><label for="q6826251:19_answer2" class="m-l-1">C. 非对称数字用户线（ADSL）</label> </div>
<div class="r1"><input type="radio" name="q6826251:19_answer" value="3" id="q6826251:19_answer3" /><label for="q6826251:19_answer3" class="m-l-1">D. 光纤分布式数据接口（FDDI）</label> </div>
</div></div></div></div></div><div id="q20" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">19</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:20_:flagged" value="0" /><input type="checkbox" id="q6826251:20_:flaggedcheckbox" name="q6826251:20_:flagged" value="1" /><input type="hidden" value="qaid=112217892&amp;qubaid=6826251&amp;qid=1605772&amp;slot=20&amp;checksum=7b550293b856b68e177e470bb12b7fb2&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:20_:flaggedlabel" for="q6826251:20_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:20_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:20_:sequencecheck" value="1" /><div class="qtext"><p>在计算机网络中，通常所说的WLAN是指（ ）。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:20_answer" value="0" id="q6826251:20_answer0" /><label for="q6826251:20_answer0" class="m-l-1">A. 城域网</label> </div>
<div class="r1"><input type="radio" name="q6826251:20_answer" value="1" id="q6826251:20_answer1" /><label for="q6826251:20_answer1" class="m-l-1">B. 广域网</label> </div>
<div class="r0"><input type="radio" name="q6826251:20_answer" value="2" id="q6826251:20_answer2" /><label for="q6826251:20_answer2" class="m-l-1">C. 无线局域网</label> </div>
<div class="r1"><input type="radio" name="q6826251:20_answer" value="3" id="q6826251:20_answer3" /><label for="q6826251:20_answer3" class="m-l-1">D. 对等网</label> </div>
</div></div></div></div></div><div id="q21" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">20</span></h3><div class="state">还未回答</div><div class="grade">满分3.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:21_:flagged" value="0" /><input type="checkbox" id="q6826251:21_:flaggedcheckbox" name="q6826251:21_:flagged" value="1" /><input type="hidden" value="qaid=112217893&amp;qubaid=6826251&amp;qid=1605773&amp;slot=21&amp;checksum=084fe04d65a1901cc20437a88daed0b7&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:21_:flaggedlabel" for="q6826251:21_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:21_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:21_:sequencecheck" value="1" /><div class="qtext"><p>无线局域网使用（ ）作为传输介质。</p></div><div class="ablock"><div class="prompt">选择一项：</div><div class="answer"><div class="r0"><input type="radio" name="q6826251:21_answer" value="0" id="q6826251:21_answer0" /><label for="q6826251:21_answer0" class="m-l-1">A. 双绞线</label> </div>
<div class="r1"><input type="radio" name="q6826251:21_answer" value="1" id="q6826251:21_answer1" /><label for="q6826251:21_answer1" class="m-l-1">B. 光纤</label> </div>
<div class="r0"><input type="radio" name="q6826251:21_answer" value="2" id="q6826251:21_answer2" /><label for="q6826251:21_answer2" class="m-l-1">C. 无线电波</label> </div>
<div class="r1"><input type="radio" name="q6826251:21_answer" value="3" id="q6826251:21_answer3" /><label for="q6826251:21_answer3" class="m-l-1">D. 同轴电缆</label> </div>
</div></div></div></div></div><div id="q22" class="que description informationitem notyetanswered"><div class="info"><div class="state"></div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:22_:flagged" value="0" /><input type="checkbox" id="q6826251:22_:flaggedcheckbox" name="q6826251:22_:flagged" value="1" /><input type="hidden" value="qaid=112217894&amp;qubaid=6826251&amp;qid=1605774&amp;slot=22&amp;checksum=e12d5f50717c3983da84f62e09529cff&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:22_:flaggedlabel" for="q6826251:22_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:22_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">信息文本</h4><input type="hidden" name="q6826251:22_:sequencecheck" value="1" /><div class="qtext"><p>二．多选题（每题4分，共40分）</p></div><div class="im-controls"><input type="hidden" name="q6826251:22_-seen" value="1" /></div></div></div></div><div id="q23" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">21</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:23_:flagged" value="0" /><input type="checkbox" id="q6826251:23_:flaggedcheckbox" name="q6826251:23_:flagged" value="1" /><input type="hidden" value="qaid=112217895&amp;qubaid=6826251&amp;qid=1605775&amp;slot=23&amp;checksum=3aca8389035b9d92a52abb2eead65bed&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:23_:flaggedlabel" for="q6826251:23_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:23_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:23_:sequencecheck" value="1" /><div class="qtext"><p>一个完整的计算机网络必须包含（ ）、（ ）、（ ）和网络协议等四个要素。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:23_choice0" value="0" /><input type="checkbox" name="q6826251:23_choice0" value="1" id="q6826251:23_choice0" /><label for="q6826251:23_choice0" class="m-l-1">A. 计算机系统</label> </div>
<div class="r1"><input type="hidden" name="q6826251:23_choice1" value="0" /><input type="checkbox" name="q6826251:23_choice1" value="1" id="q6826251:23_choice1" /><label for="q6826251:23_choice1" class="m-l-1">B. 共享的资源</label> </div>
<div class="r0"><input type="hidden" name="q6826251:23_choice2" value="0" /><input type="checkbox" name="q6826251:23_choice2" value="1" id="q6826251:23_choice2" /><label for="q6826251:23_choice2" class="m-l-1">C. 传输介质</label> </div>
<div class="r1"><input type="hidden" name="q6826251:23_choice3" value="0" /><input type="checkbox" name="q6826251:23_choice3" value="1" id="q6826251:23_choice3" /><label for="q6826251:23_choice3" class="m-l-1">D. 光纤</label> </div>
</div></div></div></div></div><div id="q24" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">22</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:24_:flagged" value="0" /><input type="checkbox" id="q6826251:24_:flaggedcheckbox" name="q6826251:24_:flagged" value="1" /><input type="hidden" value="qaid=112217896&amp;qubaid=6826251&amp;qid=1605776&amp;slot=24&amp;checksum=8e6feb9822ba8752e7b4d02ba18d6423&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:24_:flaggedlabel" for="q6826251:24_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:24_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:24_:sequencecheck" value="1" /><div class="qtext"><p>计算机网络中，实现数据交换的方法主要有（ ）、（ ）和（ ）。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:24_choice0" value="0" /><input type="checkbox" name="q6826251:24_choice0" value="1" id="q6826251:24_choice0" /><label for="q6826251:24_choice0" class="m-l-1">A. 电路交换</label> </div>
<div class="r1"><input type="hidden" name="q6826251:24_choice1" value="0" /><input type="checkbox" name="q6826251:24_choice1" value="1" id="q6826251:24_choice1" /><label for="q6826251:24_choice1" class="m-l-1">B. 报文交换</label> </div>
<div class="r0"><input type="hidden" name="q6826251:24_choice2" value="0" /><input type="checkbox" name="q6826251:24_choice2" value="1" id="q6826251:24_choice2" /><label for="q6826251:24_choice2" class="m-l-1">C. 分组交换</label> </div>
<div class="r1"><input type="hidden" name="q6826251:24_choice3" value="0" /><input type="checkbox" name="q6826251:24_choice3" value="1" id="q6826251:24_choice3" /><label for="q6826251:24_choice3" class="m-l-1">D. 帧交换</label> </div>
</div></div></div></div></div><div id="q25" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">23</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:25_:flagged" value="0" /><input type="checkbox" id="q6826251:25_:flaggedcheckbox" name="q6826251:25_:flagged" value="1" /><input type="hidden" value="qaid=112217897&amp;qubaid=6826251&amp;qid=1605777&amp;slot=25&amp;checksum=060116f10517ffde936d4424a7ee46cd&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:25_:flaggedlabel" for="q6826251:25_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:25_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:25_:sequencecheck" value="1" /><div class="qtext"><p>TCP/IP模型包含（ ）、（ ）、（ ）和网络接口层四个层次。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:25_choice0" value="0" /><input type="checkbox" name="q6826251:25_choice0" value="1" id="q6826251:25_choice0" /><label for="q6826251:25_choice0" class="m-l-1">A. 应用层</label> </div>
<div class="r1"><input type="hidden" name="q6826251:25_choice1" value="0" /><input type="checkbox" name="q6826251:25_choice1" value="1" id="q6826251:25_choice1" /><label for="q6826251:25_choice1" class="m-l-1">B. 传输层</label> </div>
<div class="r0"><input type="hidden" name="q6826251:25_choice2" value="0" /><input type="checkbox" name="q6826251:25_choice2" value="1" id="q6826251:25_choice2" /><label for="q6826251:25_choice2" class="m-l-1">C. 网际层</label> </div>
<div class="r1"><input type="hidden" name="q6826251:25_choice3" value="0" /><input type="checkbox" name="q6826251:25_choice3" value="1" id="q6826251:25_choice3" /><label for="q6826251:25_choice3" class="m-l-1">D. 数据链路层</label> </div>
</div></div></div></div></div><div id="q26" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">24</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:26_:flagged" value="0" /><input type="checkbox" id="q6826251:26_:flaggedcheckbox" name="q6826251:26_:flagged" value="1" /><input type="hidden" value="qaid=112217898&amp;qubaid=6826251&amp;qid=1605778&amp;slot=26&amp;checksum=466711d9631b562392435616f82b531c&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:26_:flaggedlabel" for="q6826251:26_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:26_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:26_:sequencecheck" value="1" /><div class="qtext"><p>局域网中，LLC子层的服务访问点SAP具有帧的（ ）和（ ）功能。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:26_choice0" value="0" /><input type="checkbox" name="q6826251:26_choice0" value="1" id="q6826251:26_choice0" /><label for="q6826251:26_choice0" class="m-l-1">A. 地址识别</label> </div>
<div class="r1"><input type="hidden" name="q6826251:26_choice1" value="0" /><input type="checkbox" name="q6826251:26_choice1" value="1" id="q6826251:26_choice1" /><label for="q6826251:26_choice1" class="m-l-1">B. 校验</label> </div>
<div class="r0"><input type="hidden" name="q6826251:26_choice2" value="0" /><input type="checkbox" name="q6826251:26_choice2" value="1" id="q6826251:26_choice2" /><label for="q6826251:26_choice2" class="m-l-1">C. 发送</label> </div>
<div class="r1"><input type="hidden" name="q6826251:26_choice3" value="0" /><input type="checkbox" name="q6826251:26_choice3" value="1" id="q6826251:26_choice3" /><label for="q6826251:26_choice3" class="m-l-1">D. 接收</label> </div>
</div></div></div></div></div><div id="q27" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">25</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:27_:flagged" value="0" /><input type="checkbox" id="q6826251:27_:flaggedcheckbox" name="q6826251:27_:flagged" value="1" /><input type="hidden" value="qaid=112217899&amp;qubaid=6826251&amp;qid=1605779&amp;slot=27&amp;checksum=ac0311362e482dc645b3ba77b9de57e6&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:27_:flaggedlabel" for="q6826251:27_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:27_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:27_:sequencecheck" value="1" /><div class="qtext"><p>无线局域网的设备主要包括（ ）、（ ）、（ ）、和无线网关、无线网桥等。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:27_choice0" value="0" /><input type="checkbox" name="q6826251:27_choice0" value="1" id="q6826251:27_choice0" /><label for="q6826251:27_choice0" class="m-l-1">A. 无线接入点</label> </div>
<div class="r1"><input type="hidden" name="q6826251:27_choice1" value="0" /><input type="checkbox" name="q6826251:27_choice1" value="1" id="q6826251:27_choice1" /><label for="q6826251:27_choice1" class="m-l-1">B. 无线路由器</label> </div>
<div class="r0"><input type="hidden" name="q6826251:27_choice2" value="0" /><input type="checkbox" name="q6826251:27_choice2" value="1" id="q6826251:27_choice2" /><label for="q6826251:27_choice2" class="m-l-1">C. 无线网卡</label> </div>
<div class="r1"><input type="hidden" name="q6826251:27_choice3" value="0" /><input type="checkbox" name="q6826251:27_choice3" value="1" id="q6826251:27_choice3" /><label for="q6826251:27_choice3" class="m-l-1">D. 卫星</label> </div>
</div></div></div></div></div><div id="q28" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">26</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:28_:flagged" value="0" /><input type="checkbox" id="q6826251:28_:flaggedcheckbox" name="q6826251:28_:flagged" value="1" /><input type="hidden" value="qaid=112217900&amp;qubaid=6826251&amp;qid=1605780&amp;slot=28&amp;checksum=507e05144b20c3b94c9cbafed5a12794&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:28_:flaggedlabel" for="q6826251:28_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:28_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:28_:sequencecheck" value="1" /><div class="qtext"><p>在转发数据帧时，交换机可采取两种模式，分别为（ ）和（ ）。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:28_choice0" value="0" /><input type="checkbox" name="q6826251:28_choice0" value="1" id="q6826251:28_choice0" /><label for="q6826251:28_choice0" class="m-l-1">A. 存储转发</label> </div>
<div class="r1"><input type="hidden" name="q6826251:28_choice1" value="0" /><input type="checkbox" name="q6826251:28_choice1" value="1" id="q6826251:28_choice1" /><label for="q6826251:28_choice1" class="m-l-1">B. 直接转发</label> </div>
<div class="r0"><input type="hidden" name="q6826251:28_choice2" value="0" /><input type="checkbox" name="q6826251:28_choice2" value="1" id="q6826251:28_choice2" /><label for="q6826251:28_choice2" class="m-l-1">C. 帧转发</label> </div>
<div class="r1"><input type="hidden" name="q6826251:28_choice3" value="0" /><input type="checkbox" name="q6826251:28_choice3" value="1" id="q6826251:28_choice3" /><label for="q6826251:28_choice3" class="m-l-1">D. 包转发</label> </div>
</div></div></div></div></div><div id="q29" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">27</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:29_:flagged" value="0" /><input type="checkbox" id="q6826251:29_:flaggedcheckbox" name="q6826251:29_:flagged" value="1" /><input type="hidden" value="qaid=112217901&amp;qubaid=6826251&amp;qid=1605781&amp;slot=29&amp;checksum=b70560293d1978898ea3b60ce849cfea&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:29_:flaggedlabel" for="q6826251:29_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:29_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:29_:sequencecheck" value="1" /><div class="qtext"><p>光纤传输系统具有（ ）、（ ）及探测器三个要素。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:29_choice0" value="0" /><input type="checkbox" name="q6826251:29_choice0" value="1" id="q6826251:29_choice0" /><label for="q6826251:29_choice0" class="m-l-1">A. 光源</label> </div>
<div class="r1"><input type="hidden" name="q6826251:29_choice1" value="0" /><input type="checkbox" name="q6826251:29_choice1" value="1" id="q6826251:29_choice1" /><label for="q6826251:29_choice1" class="m-l-1">B. 光纤</label> </div>
<div class="r0"><input type="hidden" name="q6826251:29_choice2" value="0" /><input type="checkbox" name="q6826251:29_choice2" value="1" id="q6826251:29_choice2" /><label for="q6826251:29_choice2" class="m-l-1">C. 电缆</label> </div>
<div class="r1"><input type="hidden" name="q6826251:29_choice3" value="0" /><input type="checkbox" name="q6826251:29_choice3" value="1" id="q6826251:29_choice3" /><label for="q6826251:29_choice3" class="m-l-1">D. 转换器</label> </div>
</div></div></div></div></div><div id="q30" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">28</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:30_:flagged" value="0" /><input type="checkbox" id="q6826251:30_:flaggedcheckbox" name="q6826251:30_:flagged" value="1" /><input type="hidden" value="qaid=112217902&amp;qubaid=6826251&amp;qid=1605782&amp;slot=30&amp;checksum=6a873ae65d1aa8d5add735881186ceeb&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:30_:flaggedlabel" for="q6826251:30_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:30_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:30_:sequencecheck" value="1" /><div class="qtext"><p>局域网通信协议需要解决帧定界、（ ）和（ ）这三个基本问题。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:30_choice0" value="0" /><input type="checkbox" name="q6826251:30_choice0" value="1" id="q6826251:30_choice0" /><label for="q6826251:30_choice0" class="m-l-1">A. 拓扑结构</label> </div>
<div class="r1"><input type="hidden" name="q6826251:30_choice1" value="0" /><input type="checkbox" name="q6826251:30_choice1" value="1" id="q6826251:30_choice1" /><label for="q6826251:30_choice1" class="m-l-1">B. 透明传输</label> </div>
<div class="r0"><input type="hidden" name="q6826251:30_choice2" value="0" /><input type="checkbox" name="q6826251:30_choice2" value="1" id="q6826251:30_choice2" /><label for="q6826251:30_choice2" class="m-l-1">C. 差错检测</label> </div>
<div class="r1"><input type="hidden" name="q6826251:30_choice3" value="0" /><input type="checkbox" name="q6826251:30_choice3" value="1" id="q6826251:30_choice3" /><label for="q6826251:30_choice3" class="m-l-1">D. 标准</label> </div>
</div></div></div></div></div><div id="q31" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">29</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:31_:flagged" value="0" /><input type="checkbox" id="q6826251:31_:flaggedcheckbox" name="q6826251:31_:flagged" value="1" /><input type="hidden" value="qaid=112217903&amp;qubaid=6826251&amp;qid=1605783&amp;slot=31&amp;checksum=0da89b744446a73f59c4bf06e55e9ba6&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:31_:flaggedlabel" for="q6826251:31_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:31_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:31_:sequencecheck" value="1" /><div class="qtext"><p>数据链路层的常用信道有两种，即（ ）和（ ）。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:31_choice0" value="0" /><input type="checkbox" name="q6826251:31_choice0" value="1" id="q6826251:31_choice0" /><label for="q6826251:31_choice0" class="m-l-1">A. 连接信道</label> </div>
<div class="r1"><input type="hidden" name="q6826251:31_choice1" value="0" /><input type="checkbox" name="q6826251:31_choice1" value="1" id="q6826251:31_choice1" /><label for="q6826251:31_choice1" class="m-l-1">B. 点对点信道</label> </div>
<div class="r0"><input type="hidden" name="q6826251:31_choice2" value="0" /><input type="checkbox" name="q6826251:31_choice2" value="1" id="q6826251:31_choice2" /><label for="q6826251:31_choice2" class="m-l-1">C. 广播信道</label> </div>
<div class="r1"><input type="hidden" name="q6826251:31_choice3" value="0" /><input type="checkbox" name="q6826251:31_choice3" value="1" id="q6826251:31_choice3" /><label for="q6826251:31_choice3" class="m-l-1">D. 拨号信道</label> </div>
</div></div></div></div></div><div id="q32" class="que multichoice deferredfeedback notyetanswered"><div class="info"><h3 class="no">题目<span class="qno">30</span></h3><div class="state">还未回答</div><div class="grade">满分4.00</div><div class="questionflag editable" aria-atomic="true" aria-relevant="text" aria-live="assertive"><input type="hidden" name="q6826251:32_:flagged" value="0" /><input type="checkbox" id="q6826251:32_:flaggedcheckbox" name="q6826251:32_:flagged" value="1" /><input type="hidden" value="qaid=112217904&amp;qubaid=6826251&amp;qid=1605784&amp;slot=32&amp;checksum=068a385fe81796ed67a9c5a526bf4e98&amp;sesskey=UjZLOQhC3W&amp;newstate=" class="questionflagpostdata" /><label id="q6826251:32_:flaggedlabel" for="q6826251:32_:flaggedcheckbox"><img src="http://hubei.ouchn.cn/theme/image.php/blueonionres/core/1587093656/i/unflagged" alt="未标记" id="q6826251:32_:flaggedimg" /></label>
</div></div><div class="content"><div class="formulation clearfix"><h4 class="accesshide">题干</h4><input type="hidden" name="q6826251:32_:sequencecheck" value="1" /><div class="qtext"><p>ADSL接入网由（ ）、（ ）和（ ）三大部分组成。</p></div><div class="ablock"><div class="prompt">选择一项或多项：</div><div class="answer"><div class="r0"><input type="hidden" name="q6826251:32_choice0" value="0" /><input type="checkbox" name="q6826251:32_choice0" value="1" id="q6826251:32_choice0" /><label for="q6826251:32_choice0" class="m-l-1">A. 数字用户线接入复用器</label> </div>
<div class="r1"><input type="hidden" name="q6826251:32_choice1" value="0" /><input type="checkbox" name="q6826251:32_choice1" value="1" id="q6826251:32_choice1" /><label for="q6826251:32_choice1" class="m-l-1">B. 光纤</label> </div>
<div class="r0"><input type="hidden" name="q6826251:32_choice2" value="0" /><input type="checkbox" name="q6826251:32_choice2" value="1" id="q6826251:32_choice2" /><label for="q6826251:32_choice2" class="m-l-1">C. 用户线</label> </div>
<div class="r1"><input type="hidden" name="q6826251:32_choice3" value="0" /><input type="checkbox" name="q6826251:32_choice3" value="1" id="q6826251:32_choice3" /><label for="q6826251:32_choice3" class="m-l-1">D. 用户设施</label> </div>
</div></div></div></div></div><div class="submitbtns"><input type="submit" name="next" value="结束答题…" class="mod_quiz-next-nav btn btn-primary" /></div><input type="hidden" name="attempt" value="6825060" /><input type="hidden" name="thispage" value="0" id="followingpage" /><input type="hidden" name="nextpage" value="-1" /><input type="hidden" name="timeup" value="0" id="timeup" /><input type="hidden" name="sesskey" value="UjZLOQhC3W" /><input type="hidden" name="scrollpos" value="" id="scrollpos" /><input type="hidden" name="slots" value="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32" /></div></form><div id="connection-error" style="display: none;" role="alert"><p>网络连接断开（自动保存失败）。</p>

<p>请记录下最近几分钟在本页面所键入的答题结果，然后尝试重新连接。</p>

<p>一旦连接被重新建立，你的答题结果将会被自动保存，同时这个消息会消失。</p>
</div><div id="connection-ok" style="display: none;" role="alert"><p>网络连接恢复。你可以继续安全使用。</p>
</div></div>
                    
                    </div>
                </section>
                <section data-region="blocks-column" class="hidden-print">
                    <aside id="block-region-side-pre" class="block-region" data-blockregion="side-pre" data-droptarget="1"><a href="#sb-1" class="sr-only sr-only-focusable">跳过 &lt;span id=&quot;mod_quiz_navblock_title&quot;&gt;测验导航&lt;/span&gt;</a>

<aside id="mod_quiz_navblock"
     class=" block block__fake  card m-b-1"
     role="navigation"
     data-block="_fake"
          aria-labelledby="instance-0-header"
     >

    <div class="card-block">


            <h3 id="instance-0-header" class="card-title"><span id="mod_quiz_navblock_title">测验导航</span></h3>

        <div class="card-text content">
            <div id="quiznojswarning">警告：这些链接不会保存你的答案。请使用页面底端的下一步按钮。</div><div class="qn_buttons clearfix multipages"><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton1" title="还未看过" data-quiz-page="0" href="#"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">信息</span> 信息<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton2" title="还未回答" data-quiz-page="0" href="#q2"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 1<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton3" title="还未回答" data-quiz-page="0" href="#q3"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 2<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton4" title="还未回答" data-quiz-page="0" href="#q4"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 3<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton5" title="还未回答" data-quiz-page="0" href="#q5"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 4<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton6" title="还未回答" data-quiz-page="0" href="#q6"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 5<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton7" title="还未回答" data-quiz-page="0" href="#q7"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 6<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton8" title="还未回答" data-quiz-page="0" href="#q8"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 7<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton9" title="还未回答" data-quiz-page="0" href="#q9"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 8<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton10" title="还未回答" data-quiz-page="0" href="#q10"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 9<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton11" title="还未回答" data-quiz-page="0" href="#q11"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 10<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton12" title="还未回答" data-quiz-page="0" href="#q12"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 11<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton13" title="还未回答" data-quiz-page="0" href="#q13"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 12<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton14" title="还未回答" data-quiz-page="0" href="#q14"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 13<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton15" title="还未回答" data-quiz-page="0" href="#q15"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 14<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton16" title="还未回答" data-quiz-page="0" href="#q16"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 15<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton17" title="还未回答" data-quiz-page="0" href="#q17"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 16<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton18" title="还未回答" data-quiz-page="0" href="#q18"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 17<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton19" title="还未回答" data-quiz-page="0" href="#q19"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 18<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton20" title="还未回答" data-quiz-page="0" href="#q20"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 19<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton21" title="还未回答" data-quiz-page="0" href="#q21"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 20<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton22" title="还未看过" data-quiz-page="0" href="#q22"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">信息</span> 信息<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton23" title="还未回答" data-quiz-page="0" href="#q23"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 21<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton24" title="还未回答" data-quiz-page="0" href="#q24"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 22<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton25" title="还未回答" data-quiz-page="0" href="#q25"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 23<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton26" title="还未回答" data-quiz-page="0" href="#q26"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 24<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton27" title="还未回答" data-quiz-page="0" href="#q27"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 25<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton28" title="还未回答" data-quiz-page="0" href="#q28"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 26<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton29" title="还未回答" data-quiz-page="0" href="#q29"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 27<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton30" title="还未回答" data-quiz-page="0" href="#q30"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 28<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton31" title="还未回答" data-quiz-page="0" href="#q31"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 29<span class="accesshide"> 此页 <span class="flagstate"></span></span></a><a class="qnbutton notyetanswered free btn btn-secondary thispage" id="quiznavbutton32" title="还未回答" data-quiz-page="0" href="#q32"><span class="thispageholder"></span><span class="trafficlight"></span><span class="accesshide">题目</span> 30<span class="accesshide"> 此页 <span class="flagstate"></span></span></a></div><div class="othernav"><a class="endtestlink" href="http://hubei.ouchn.cn/mod/quiz/summary.php?attempt=6825060">结束答题…</a><div id="quiz-timer" role="timer" aria-atomic="true" aria-relevant="text">剩余时间 <span id="quiz-time-left"></span></div></div>
            <div class="footer"></div>
            
        </div>

    </div>

</aside>

  <span id="sb-1"></span></aside>
                </section>
            </div>
        </div>
    </div>
    <div id="nav-drawer"  data-region="drawer" class="hidden-print moodle-has-zindex closed" aria-hidden="true" tabindex="-1">
        <nav class="list-group">
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=5284" data-key="coursehome">
                <div class="m-l-0">
                        网络实用技术基础
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/user/index.php?id=5284" data-key="participants">
                <div class="m-l-0">
                        成员
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/badges/view.php?type=2&amp;id=5284" data-key="badgesview">
                <div class="m-l-0">
                        勋章
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/grade/report/index.php?id=5284" data-key="grades">
                <div class="m-l-0">
                        成绩
                </div>
            </a>
        </nav>
        <nav class="list-group m-t-1">
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/my/" data-key="myhome">
                <div class="m-l-0">
                        个人主页
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/?redirect=0" data-key="home">
                <div class="m-l-0">
                        网站首页
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/calendar/view.php?view=month" data-key="calendar">
                <div class="m-l-0">
                        日程管理
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/user/files.php" data-key="privatefiles">
                <div class="m-l-0">
                        私人文件
                </div>
            </a>
            <div class="list-group-item" data-key="mycourses">
                <div class="m-l-0">
                    我的课程
                </div>
            </div>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=4648" data-key="4648">
                <div class="m-l-1">
                        习近平新时代中国特色社会主义思想
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=4811" data-key="4811">
                <div class="m-l-1">
                        国家开放大学学习指南
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=4639" data-key="4639">
                <div class="m-l-1">
                        微积分基础
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=4731" data-key="4731">
                <div class="m-l-1">
                        数据库基础与应用
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=4550" data-key="4550">
                <div class="m-l-1">
                        管理信息系统
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=5284" data-key="5284">
                <div class="m-l-1">
                        网络实用技术基础
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=99" data-key="99">
                <div class="m-l-1">
                        计算机专业指南(专)
                </div>
            </a>
            <a class="list-group-item list-group-item-action " href="http://hubei.ouchn.cn/course/view.php?id=4558" data-key="4558">
                <div class="m-l-1">
                        计算机应用基础
                </div>
            </a>
        </nav>
    </div>
    <footer id="page-footer" style="min-height:70px;background-color:rgba(55,58,60,0.6) !important" class="p-y-1 bg-inverse">
    <div class="container">
    <div style="text-align:center;line-height:35px">版权所有 国家开放大学</div>
    <!--
        <div id="course-footer"></div>


        <div class="logininfo">您以<a href="http://hubei.ouchn.cn/user/profile.php?id=135249" title="查看个人资料">吴蔓</a>登录 (<a href="http://hubei.ouchn.cn/login/logout.php?sesskey=UjZLOQhC3W">退出</a>)</div>
        <div class="homelink"><a href="http://hubei.ouchn.cn/course/view.php?id=5284">01507</a></div>
        <nav class="nav navbar-nav hidden-lg-up">
                <ul class="list-unstyled p-t-1">
                                    <li><a href="http://shome.ouchn.cn" title="学生空间">学生空间</a></li>
                                    <li><a href="http://thome.ouchn.cn" title="教师空间">教师空间</a></li>
                                    <li><a href="http://hubei.ouchn.cn/course" title="所有课程">所有课程</a></li>
                </ul>
        </nav>
         -->
        <script type="text/javascript">
//<![CDATA[
var require = {
    baseUrl : 'http://hubei.ouchn.cn/lib/requirejs.php/-1/',
    // We only support AMD modules with an explicit define() statement.
    enforceDefine: true,
    skipDataMain: true,
    waitSeconds : 0,

    paths: {
        jquery: 'http://hubei.ouchn.cn/lib/javascript.php/-1/lib/jquery/jquery-3.1.0.min',
        jqueryui: 'http://hubei.ouchn.cn/lib/javascript.php/-1/lib/jquery/ui-1.12.1/jquery-ui.min',
        jqueryprivate: 'http://hubei.ouchn.cn/lib/javascript.php/-1/lib/requirejs/jquery-private'
    },

    // Custom jquery config map.
    map: {
      // '*' means all modules will get 'jqueryprivate'
      // for their 'jquery' dependency.
      '*': { jquery: 'jqueryprivate' },

      // 'jquery-private' wants the real jQuery module
      // though. If this line was not here, there would
      // be an unresolvable cyclic dependency.
      jqueryprivate: { jquery: 'jquery' }
    }
};

//]]>
</script>
<script type="text/javascript" src="http://hubei.ouchn.cn/lib/javascript.php/-1/lib/requirejs/require.min.js"></script>
<script type="text/javascript">
//<![CDATA[
require(['core/first'], function() {
;
require(["media_videojs/loader"], function(loader) {
    loader.setUp(function(videojs) {
        videojs.options.flash.swf = "http://hubei.ouchn.cn/media/player/videojs/videojs/video-js.swf";
videojs.addLanguage("zh-CN",{
 "Play": "播放",
 "Pause": "暂停",
 "Current Time": "当前时间",
 "Duration Time": "时长",
 "Remaining Time": "剩余时间",
 "Stream Type": "媒体流类型",
 "LIVE": "直播",
 "Loaded": "加载完毕",
 "Progress": "进度",
 "Fullscreen": "全屏",
 "Non-Fullscreen": "退出全屏",
 "Mute": "静音",
 "Unmute": "取消静音",
 "Playback Rate": "播放码率",
 "Subtitles": "字幕",
 "subtitles off": "字幕关闭",
 "Captions": "内嵌字幕",
 "captions off": "内嵌字幕关闭",
 "Chapters": "节目段落",
 "You aborted the media playback": "视频播放被终止",
 "A network error caused the media download to fail part-way.": "网络错误导致视频下载中途失败。",
 "The media could not be loaded, either because the server or network failed or because the format is not supported.": "视频因格式不支持或者服务器或网络的问题无法加载。",
 "The media playback was aborted due to a corruption problem or because the media used features your browser did not support.": "由于视频文件损坏或是该视频使用了你的浏览器不支持的功能，播放终止。",
 "No compatible source was found for this media.": "无法找到此视频兼容的源。",
 "The media is encrypted and we do not have the keys to decrypt it.": "视频已加密，无法解密。"
});

    });
});;

require(['theme_blueonionres/loader']);
require(['theme_blueonionres/drawer'], function(mod) {
    mod.init();
});
;
require(["core/notification"], function(amd) { amd.init(964046, []); });;
require(["core/log"], function(amd) { amd.setConfig({"level":"warn"}); });
});
//]]>
</script>
<script type="text/javascript" src="http://hubei.ouchn.cn/lib/javascript.php/-1/theme/blueonionres/jquery/jquery.js"></script>
<script type="text/javascript">
//<![CDATA[
M.str = {"moodle":{"lastmodified":"\u6700\u540e\u4fee\u6539","name":"\u540d\u79f0","error":"\u9519\u8bef","info":"\u4fe1\u606f","yes":"\u662f","no":"\u5426","cancel":"\u53d6\u6d88","changesmadereallygoaway":"\u60a8\u505a\u51fa\u4e86\u6539\u52a8\u3002\u60a8\u786e\u5b9a\u8981\u79bb\u5f00\u5e76\u653e\u5f03\u6240\u6709\u6539\u52a8\u5417\uff1f","confirm":"\u786e\u8ba4","areyousure":"\u4f60\u786e\u5b9a\u5417\uff1f","closebuttontitle":"\u5173\u95ed","unknownerror":"\u672b\u77e5\u9519\u8bef"},"repository":{"type":"\u7c7b\u578b","size":"\u5927\u5c0f","invalidjson":"\u65e0\u6548\u7684JSON\u5b57\u7b26\u4e32","nofilesattached":"\u6ca1\u6709\u9644\u4ef6","filepicker":"\u6587\u4ef6\u9009\u62e9\u5668","logout":"\u767b\u51fa","nofilesavailable":"\u6ca1\u6709\u53ef\u7528\u6587\u4ef6","norepositoriesavailable":"\u62b1\u6b49\uff0c\u60a8\u4f7f\u7528\u7684\u5bb9\u5668\u90fd\u4e0d\u80fd\u8fd4\u56de\u7b26\u5408\u9700\u8981\u7684\u683c\u5f0f\u7684\u6587\u4ef6\u3002","fileexistsdialogheader":"\u6587\u4ef6\u5df2\u5b58\u5728","fileexistsdialog_editor":"\u60a8\u6b63\u7f16\u8f91\u7684\u6587\u672c\u7684\u9644\u4ef6\u4e2d\u5df2\u7ecf\u6709\u4e00\u4e2a\u540c\u540d\u6587\u4ef6\u3002","fileexistsdialog_filemanager":"\u5df2\u7ecf\u6709\u4e00\u4e2a\u540c\u540d\u6587\u4ef6","renameto":"\u91cd\u547d\u540d\u4e3a\u201c{$a}\u201d","referencesexist":"\u6709 {$a} \u4e2a\u522b\u540d\u6216\u5feb\u6377\u65b9\u5f0f\u5f15\u7528\u6b64\u6587\u4ef6","select":"\u9009\u62e9"},"admin":{"confirmdeletecomments":"\u60a8\u5c06\u5220\u9664\u8bc4\u8bba\uff0c\u786e\u5b9a\u5417\uff1f","confirmation":"\u786e\u8ba4"},"question":{"flagged":"\u5df2\u6807\u8bb0"},"quiz":{"functiondisabledbysecuremode":"\u8be5\u529f\u80fd\u76ee\u524d\u5df2\u505c\u7528","startattempt":"\u5f00\u59cb\u7b54\u9898","timesup":"\u65f6\u95f4\u5230\uff01"}};
//]]>
</script>
<script type="text/javascript">
//<![CDATA[
(function() {Y.use("moodle-filter_mathjaxloader-loader",function() {M.filter_mathjaxloader.configure({"mathjaxconfig":"\r\nMathJax.Hub.Config({\r\n    config: [\"Accessible.js\", \"Safe.js\"],\r\n    errorSettings: { message: [\"!\"] },\r\n    skipStartupTypeset: true,\r\n    messageStyle: \"none\"\r\n});\r\n","lang":"en"});
});
Y.use("moodle-mod_quiz-autosave",function() {M.mod_quiz.autosave.init("60");
});
 M.util.js_pending('random5eb9599ea80391'); Y.use('core_question_flags', function(Y) { M.core_question_flags.init(Y, "http:\/\/hubei.ouchn.cn\/question\/toggleflag.php", [{"src":"http:\/\/hubei.ouchn.cn\/theme\/image.php\/blueonionres\/core\/1587093656\/i\/unflagged","title":"\u6807\u8bb0\u6b64\u9898\u76ee\u4f9b\u5c06\u6765\u53c2\u8003","alt":"\u672a\u6807\u8bb0"},{"src":"http:\/\/hubei.ouchn.cn\/theme\/image.php\/blueonionres\/core\/1587093656\/i\/flagged","title":"\u5220\u9664\u6807\u8bb0","alt":"\u5df2\u6807\u8bb0"}], ["\u6807\u8bb0\u9898\u76ee","\u79fb\u9664\u6807\u8bb0"]);  M.util.js_complete('random5eb9599ea80391'); });
 M.util.js_pending('random5eb9599ea80392'); Y.use('mod_quiz', function(Y) { M.mod_quiz.init_attempt_form(Y);  M.util.js_complete('random5eb9599ea80392'); });
 M.util.js_pending('random5eb9599ea80393'); Y.use('mod_quiz', function(Y) { M.mod_quiz.nav.init(Y);  M.util.js_complete('random5eb9599ea80393'); });
M.util.help_popups.setup(Y);
 M.util.js_pending('random5eb9599ea803913'); Y.on('domready', function() { M.util.js_complete("init");  M.util.js_complete('random5eb9599ea803913'); });
})();
//]]>
</script>

    </div>
</footer>
</div>


</body>
</html>'''
    html = BeautifulSoup(source, "html.parser")
    q_texts = html.find_all('div', class_='qtext')
    shitis  = ""
    for q in q_texts:
        print(q.text+"###################################################")
        shitis+=(q.text+"###################################################\r")
    data = open('test3.txt', 'w+')
    print(shitis, file=data)
    data.close()
    # file.write(shitis)
    pass

def parseShiTi(shijuan_html, attempt, sesskey, info):
    print(time.strftime('%Y-%m-%d %H:%M:%S',
                        time.localtime(time.time())) + "####### 即将解析: " + shijuan_html.title.string)
    single_answer = info.single_answer
    multi_answer = info.multi_answer
    single_timu = shijuan_html.find_all('input',
                                        attrs={'type': 'radio'})  # ('input',class_=re.compile('questionflagpostdata '))
    slots_num1 = shijuan_html.find_all('a', attrs={'data-quiz-page': '0'})
    slots_num2 = shijuan_html.find_all('a', attrs={'data-quiz-page': '1'})
    slots_num3 = shijuan_html.find_all('a', attrs={'data-quiz-page': '2'})
    slots_num4 = shijuan_html.find_all('a', attrs={'data-quiz-page': '3'})
    slots_num5 = shijuan_html.find_all('a', attrs={'data-quiz-page': '4'})
    multi_timu = []
    for multi in shijuan_html.find_all('input', attrs={'type': 'checkbox'}):
        if "choice" in multi["name"]:
            multi_timu.append(multi)
    single_data = handleSingle(single_timu, single_answer, shijuan_html)
    multi_data = handleMulti(multi_timu, multi_answer, shijuan_html)
    other_param_data = hanle_auto_save_param(sesskey, attempt,
                                             len(slots_num1) + len(slots_num2) + len(slots_num3) + len(
                                                 slots_num4) + len(slots_num5))
    param_data = single_data + multi_data + other_param_data
    return param_data


# 处理单选题
def handleSingle(single_timu, single_answer, shijuan_html):
    single_list = []
    for single in single_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        single_list.append(choice_content.string)
    single_groups = list_of_groups(single_list, 4)
    parse_single_list = parseSingle2List(single_answer)
    right_answer = []
    i = 0
    for answer in parse_single_list:
        if "." in answer:
            answer = answer.split(".")[1]
        for answers in single_groups[i]:
            if answer in answers:
                right_answer.append(answers)
        i += 1
    label_list = []
    right_id_list = []
    for single in single_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        label_list.append(choice_content)
    for r_an in right_answer:
        for label in label_list:
            if r_an == label.string:
                right_id_list.append(label['for'])
    right_answers_map = {}
    for id in right_id_list:
        right_answers_map[id[0:-1]] = id[-1]
    single_auto_save_data = ""
    for k, v in right_answers_map.items():
        temp = (k + "=" + v + "&" + k[0:-6] + ":flagged=0&" + (k[0:-6] + ":flagged=0&") + (
                    k[0:-6] + ":sequencecheck=1&"))
        single_auto_save_data += temp
    return single_auto_save_data


# 处理多选题
def handleMulti(multi_timu, multi_answer, shijuan_html):
    multi_list = []
    for single in multi_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        multi_list.append(choice_content.string)
    multi_groups = list_of_groups(multi_list, 4)
    parse_multi_list = parseMulti2List(multi_answer)
    right_answer = []
    i = 0
    for multi_row_answers in parse_multi_list:
        for an in multi_row_answers:
            for xuanxiang in multi_groups[i]:
                if an in xuanxiang:
                    right_answer.append(xuanxiang)
        i += 1

    label_list = []
    right_id_list = []
    for single in multi_timu:
        choice_content = shijuan_html.find('label', attrs={'for': single['id']})
        label_list.append(choice_content)
    for r_an in right_answer:
        for label in label_list:
            if r_an == label.string:
                right_id_list.append(label['for'])
    right_answers_map = {}
    for id in right_id_list:
        right_answers_map[id] = "1"
    single_auto_save_data = ""
    for k, v in right_answers_map.items():
        temp = (k + "=" + v + "&" + k[0:-7] + ":flagged=0&" + (k[0:-7] + ":flagged=0&") + (
                k[0:-7] + ":sequencecheck=1&"))
        single_auto_save_data += temp
    return single_auto_save_data


# 将列表按指定长度切割多份
def list_of_groups(list_info, per_list_len):
    '''
    :param list_info:   列表
    :param per_list_len:  每个小列表的长度
    :return:
    '''
    list_of_group = zip(*(iter(list_info),) * per_list_len)
    end_list = [list(i) for i in list_of_group]  # i is a tuple
    count = len(list_info) % per_list_len
    end_list.append(list_info[-count:]) if count != 0 else end_list
    return end_list


# 将单选题答案处理成list返回
def parseSingle2List(single_answer):
    single_list = []
    answers = single_answer.split("\n")
    for answer in answers:
        if len(answer.strip()) > 1:
            single_list.append(answer.strip())
    return single_list


# 处理autoSave接口的其它必填参数
def hanle_auto_save_param(sesskey, attempt, timu_num):
    other_params_auto_save_data = ""
    other_params = {}
    other_params['next'] = '结束答题…'
    other_params['attempt'] = attempt
    other_params['thispage'] = '0'
    other_params['nextpage'] = '-1'
    other_params['timeup'] = '0'
    other_params['sesskey'] = sesskey
    other_params['scrollpos'] = ''
    slots = []
    for i in range(timu_num):
        slots.append(str(i + 1))
    other_params['slots'] = ",".join(slots)
    for k, v in other_params.items():
        temp = (k + "=" + v + "&")
        other_params_auto_save_data += temp
    return other_params_auto_save_data[0:-1]


# 解析试题页
def parseMulti2List(multi_answer):
    multi_list = []
    answers = multi_answer.split("\n")
    for answer in answers:
        if len(answer.strip()) > 1:
            multi_row_answers = []
            if "." in answer:
                answer = answer.split(".")[1]
            for an in answer.split("；"):
                multi_row_answers.append(an.strip())
            multi_list.append(multi_row_answers)
    return multi_list


# python取指定前后字符中间
def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


# 从科目名txt取账号构成字典
def getAcounts(course_name):
    acounts = {}
    file = open(course_name + '.txt')
    keys = []
    for line in file.readlines():
        keys.append(line.strip())

    for key in keys:
        username = key.split("\t")[0]
        password = key.split("\t")[1]
        acounts[username] = password
    return acounts


# 从带数字的科目名txt中取出所有完成形考obj
def getImportantInfo(course_name):
    infos = []
    curdir = os.path.curdir
    filenames = os.listdir(curdir)
    tiku_files = []
    for filename in filenames:
        if ".txt" in filename and course_name in filename and len(filename) > len(course_name + ".txt"):
            tiku_files.append(filename)
    for tiku_name in tiku_files:
        file = open(tiku_name, "r", encoding='UTF-8')
        info = important_info("", "", "", "")
        single_flag = False
        multi_flag = False
        judge_flag = False
        single_answer = ""
        multi_answer = ""
        judge_answer = ""
        for line in file.readlines():
            if line.strip() == "":
                single_flag = False
                multi_flag = False
                judge_flag = False
            elif "quiz/view" in line:
                info.cmid = line.split("id=")[1].strip()
            elif "单选题" in line or "单向选择题" in line:
                single_flag = True
            elif "多选题" in line or "多向选择题" in line:
                multi_flag = True
            elif "判断题" in line:
                judge_flag = True
            elif single_flag:
                single_answer += line
            elif multi_flag:
                multi_answer += line
            elif judge_flag:
                judge_answer += line
        info.single_answer = single_answer
        info.multi_answer = multi_answer
        info.judge_answer = judge_answer
        infos.append(info)
    return infos


if __name__ == '__main__':
    testFinal()
    course_name = "网络实用技术基础"
    infos = getImportantInfo(course_name)
    # 先拿到账号字典
    acounts = getAcounts(course_name)

    # 老平台登录后进新平台的第一个post所需header
    headers = {'Host': 'hubei.ouchn.cn',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Origin': 'http://shome.ouchn.cn',
               'Cookie': 'CheckCode=6SC8BtjY/n4=',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9'}
    headers2 = {'Host': 'hubei.ouchn.cn',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Origin': 'http://hubei.ouchn.cn',
                'Upgrade-Insecure-Requests': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9'}
    headers3 = {'Host': 'hubei.ouchn.cn',
                'Connection': 'keep-alive',
                'Origin': 'http://hubei.ouchn.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9'}

    # 所有账号分别登录
    acount_i = 0
    for k, v in acounts.items():
        acount_i += 1
        print(time.strftime('%Y-%m-%d %H:%M:%S',
                            time.localtime(time.time())) + "####### 程序即将处理第[" + str(acount_i) + "]个账号: " + k)
        # 一个账号只用登录一次便可完成该科目所有形考
        student_name = ""
        # 登录,能拿到tokenId
        login_url = "http://sso.ouchn.cn/Passport/AjaxLogin?lu=" + k + "&lp=" + v + "&ru=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLoginCallback&to=20200509&ip=%3A%3Affff%3A172.16.4.87&aid=11&lou=http%3A%2F%2Fpassport.ouchn.cn%2FAccount%2FLogout&sf=e57e97bdb5c64b7a&_=1588910077684"
        result1 = requests.get(url=login_url)
        if ":true," not in result1.text:
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())) + "####### 第[" + str(acount_i) + "]个账号: " + k + " 登录失败,请用网页端检查账号密码是否无误.跳过该账号.")
            continue
        # 在html里拿认证的url
        login_url = "http://shome.ouchn.cn/Learn/Course/GetMoodleHub?site=http://hubei.ouchn.cn&rid=4&courseCode=01507&cid=c89531f3-ca83-4d78-810a-fe4755b85a66"
        result1 = requests.get(url=login_url, cookies=result1.cookies)
        html1 = BeautifulSoup(result1.text, "html.parser")
        find_all = html1.find_all('form', limit=1)
        sessKey_post_data = html1.find_all('input')[-1]
        value_ = sessKey_post_data['value']
        quote = urllib.parse.quote(value_)
        get_MoodleSession_url = find_all[0]['action']
        # 此处经常签名错误,故做报错重试机制
        retry_num = 0
        while (retry_num < 3):
            retry_num += 1
            # 此处重定向是重头戏,python会自动调用最后个那个重定向后的接口
            chongdingxiang_result = requests.post(url=get_MoodleSession_url,
                                                  data='CourseClass='+quote,# 2020年5月11日21:36:41此处是陈骁用fiddle告知必须正确传参才能保证不会签名错误.吸取教训,不该偷懒
                                                  headers=headers)
            time.sleep(3)
            sesskey = getmidstring(chongdingxiang_result.text, "sesskey\":\"", "\",\"themerev")
            if sesskey is not None:
                student_name = getmidstring(chongdingxiang_result.text, '查看个人资料">', '<')
                print(time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.localtime(time.time())) + "####### " + student_name + " 已登录")
                break
            print("重定向请求出错,正在进行第" + str(retry_num) + "次尝试...")
        if retry_num > 2:
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())) + "####### 第[" + str(acount_i) + "]个账号: " + k + "多次重定向出错,跳过该账号.")
            continue
        result_history = chongdingxiang_result.history
        # 一个账号考完所有形考
        for info in infos:
            cmid = info.cmid  # 形考url的末尾id
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time())) + "####### " + student_name + " 即将处理形考id: " + cmid)
            # 判断下这个人是否已经考过该形考,且得分百分之八十以上则跳过
            before_kao_url = "http://hubei.ouchn.cn/mod/quiz/view.php?id=" + cmid
            before_kao_result = requests.get(url=before_kao_url, headers=headers2, cookies=result_history[0].cookies)
            top_score = getmidstring(before_kao_result.text, '最高分:', '<')
            if top_score is not None and len(top_score) > 1:
                score_split = top_score.split("/")
                if (float(score_split[0].strip()) / float(score_split[1].strip()) > 0.8):
                    print(time.strftime('%Y-%m-%d %H:%M:%S',
                                        time.localtime(
                                            time.time())) + "####### " + student_name + " 该形考最高得分已满足要求(80%),跳过该形考.")
                    continue

            get_attempt_url = "http://hubei.ouchn.cn/mod/quiz/startattempt.php"
            get_attempt_data = "cmid=" + cmid + "&sesskey=" + sesskey
            shijuan_result = requests.post(url=get_attempt_url, data=get_attempt_data, headers=headers2,
                                           cookies=result_history[0].cookies)
            time.sleep(3)
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    time.time())) + "####### " + student_name + " 已进入试卷.")
            shijuan_result_history = shijuan_result.history
            attempt = str(shijuan_result_history[0].headers['Location'])[-7:]
            shijuan_html = BeautifulSoup(shijuan_result.text, "html.parser")
            auto_save_data = parseShiTi(shijuan_html, attempt, sesskey, info)
            auto_save_urlEncode_data = urllib.parse.quote(auto_save_data)
            auto_save_urlEncode_data2 = auto_save_urlEncode_data.replace("%3D", "=")
            auto_save_urlEncode_data3 = auto_save_urlEncode_data2.replace("%26", "&")
            auto_save_url = "http://hubei.ouchn.cn/mod/quiz/autosave.ajax.php"
            auto_save_result = requests.post(url=auto_save_url, data=auto_save_urlEncode_data3, headers=headers3,
                                             cookies=result_history[0].cookies)
            time.sleep(2)
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    time.time())) + "####### " + student_name + " 已保存答案,即将提交...")
            # 提交试卷
            submit_url = "http://hubei.ouchn.cn/mod/quiz/processattempt.php"
            requests.post(url=submit_url,
                          data="attempt=" + attempt + "&finishattempt=1&timeup=0&slots=&sesskey=" + sesskey,
                          headers=headers2,
                          cookies=result_history[0].cookies)

            before_kao_url = "http://hubei.ouchn.cn/mod/quiz/view.php?id=" + cmid
            before_kao_result = requests.get(url=before_kao_url, headers=headers2, cookies=result_history[0].cookies)
            top_score = getmidstring(before_kao_result.text, '最高分:', '<')
            print(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(
                                    time.time())) + "####### " + student_name + " 已提交! 该形考得分:" + top_score)
