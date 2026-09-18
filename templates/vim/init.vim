" Windows 下无插件快速配置 Neovim
" 在命令模式下输入 :echo stdpath('config') 即可找到配置文件路径
" 配置文件名应为 init.vim
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 通用设置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let mapleader=","        " 定义<leader>键
set nocompatible         " 设置不兼容原始vi模式
filetype on              " 设置开启文件类型侦测
filetype plugin on       " 设置加载对应文件类型的插件
set noeb                 " 关闭错误的提示
syntax enable            " 开启语法高亮功能
syntax on                " 自动语法高亮
set t_Co=256             " 开启256色支持
set cmdheight=2          " 设置命令行的高度
set showcmd              " select模式下显示选中的行数
set ruler                " 总是显示光标位置
set laststatus=2         " 总是显示状态栏
set number               " 开启行号显示
" set cursorline           " 高亮显示当前行
set ttimeoutlen=0        " 设置<ESC>键响应时间
set virtualedit=block,onemore   " 允许光标出现在最后一个字符的后面
set mouse=a             " 设置鼠标模式
set autowriteall         " 自动保存
set autoread             " 文件在Vim之外修改过，自动重新读入
set autochdir            " 当前目录随着被编辑文件的改变而改变
let autosave=1           " 自动保存
set relativenumber       " 相对行号
set guifont=Consolas:h18 " 字体设置

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 代码缩进和排版
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set autoindent           " 设置自动缩进
set cindent              " 设置使用C/C++语言的自动缩进方式
set cinoptions=g0,:0,N-s,(0    " 设置C/C++语言的具体缩进方式
set smartindent          " 智能的选择对齐方式
filetype indent on       " 自适应不同语言的智能缩进
set expandtab            " 将制表符扩展为空格
set tabstop=2            " 设置编辑时制表符占用空格数
set shiftwidth=2         " 设置格式化时制表符占用空格数
set softtabstop=2        " 设置多少个空格为制表符
set smarttab             " 在行和段开始处使用制表符
set nowrap               " 禁止折行
set backspace=2          " 使用回车键正常处理indent,eol,start等
set sidescroll=10        " 设置向右滚动字符数
set nofoldenable         " 禁用折叠代码

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 代码补全
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set wildmenu             " vim自身命名行模式智能补全
set completeopt-=preview " 补全时不显示窗口，只显示补全列表

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 搜索设置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set hlsearch            " 高亮显示搜索结果
set incsearch           " 开启实时搜索功能
set ignorecase          " 搜索时大小写不敏感

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 缓存设置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set nobackup            " 设置不备份
set noswapfile          " 禁止生成临时文件
set autoread            " 文件在vim之外修改过，自动重新读入
set autowrite           " 设置自动保存
set confirm             " 在处理未保存或只读文件的时候，弹出确认

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 编码设置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set langmenu=zh_CN.UTF-8
set helplang=cn
set termencoding=utf-8
set encoding=utf8
set fileencodings=utf8,ucs-bom,gbk,cp936,gb2312,gb18030

" 分屏窗口移动
nnoremap <c-j> <c-w>j
nnoremap <c-k> <c-w>k
nnoremap <c-h> <c-w>h
nnoremap <c-l> <c-w>l

" 复制当前选中到系统剪切板
vmap <leader><leader>y "+y

" 将系统剪切板内容粘贴到vim
nnoremap <leader><leader>p "+p

" gv
nnoremap <leader>g :GV<cr>
nnoremap <leader>G :GV!<cr>
nnoremap <leader>gg :GV?<cr>

" C++ 编译命令配置
set makeprg=g++\ %\ -o%<\ -O2\ -Wall\ -Wextra\ -std=c++20\ -Wfloat-equal\ -Wconversion\ -Wlogical-op\ -DLOCAL
" set makeprg=g++\ %\ -o%<\ -Wall\ -std=c++14\ -DLOCAL\ -g

" 点击 F9 编译运行代码
nnoremap <F9> :silent call Cmp()<CR>
inoremap <F9> <Esc>:silent call Cmp()<CR>

" 点击 F10 打开输入数据文件 in
nnoremap <F10> :e in <CR>
inoremap <F10> <Esc>:e in <CR>

" 双击 \\ 键关闭除了当前窗口外的其它窗口
nnoremap \\ :only<CR>
" 组合按键 [n 跳转到下一个标签页
nnoremap [n :bn<CR>
" 组合按键 [p 跳转到下一个标签页
nnoremap [p :bp<CR>
" 组合按键 Alt和-/+ 调整窗口大小
nnoremap <M-=> :vertical resize +10<CR>
nnoremap <M--> :vertical resize -10<CR>

" Ctrl+A 复制所有内容到系统剪贴板
nnoremap <c-A> gg"+yG

" 以下为编译运行时的一些设置
" 个人习惯开一个文件夹，在里面创建 in 和 out 文件分别作为输入和输出，然后再创建一个 template.cpp 作为模板代码
" 要写程序时创建一个文件比如 A.cpp ，输入和输出都通过 in 和 out 文件，通过快捷键可以快速引入模板文件
function Set()
    if winnr('$')>1
        wincmd l
        wincmd k
        write
        wincmd t
        only
    endif
    write
endfunc

function Run()
    call Set()
    " !(time ./%< <%<.in >%<.out)2>>%<.out
    " !touch %<.in %<.out
    " !(./%< <%<.in >%<.out)2>>%<.out
    " belowright vsplit %<.in
    " belowright sview %<.out
    !touch in out
    !%<.exe <in >out
    belowright vsplit in
    belowright sview out
    wincmd t
    redraw!
endfunc

function Cmp()
    call Set()
    let v:statusmsg=''
    make
    if empty(v:statusmsg)
        call Run()
    else
        cwindow
        winc t
        redraw!
    endif
endfunc

" 组合按键 <leader><leader>f 用代码模板覆盖当前 .cpp 文件
nnoremap <leader><leader>f :silent call Flash()<CR>
function Flash()
    if expand("%:e") == 'cpp'
        !copy template.cpp %
        " !cat template.cpp >> %
    endif
endfunc

" 点击 F2 在.sh .py .cpp 文件添加作者信息和当前时间
nnoremap <F2> :silent call AutherInfo()<CR>
inoremap <F2> <Esc>:silent call AutherInfo()<CR>
function AutherInfo()
    if expand("%:e") == 'sh' || expand("%:e") == 'py'
        execute "normal ggO"
        call setline(1, "##########################################################################")
        call append(line("."), " # Author: Daniel")
        call append(line(".") + 1, " # Created Time: ".strftime("%Y-%m-%d %H:%M:%S"))
        call append(line(".") + 2, "#########################################################################")
        call append(line(".") + 3, "")
    elseif expand("%:e") == 'c' || expand("%:e") == 'cpp' || expand("%:e") == 'h'
        execute "normal ggO"
        call setline(1, "/**")
        call append(line("."), " * Author: Daniel")
        call append(line(".") + 1, " * Created Time: ".strftime("%Y-%m-%d %H:%M:%S"))
        call append(line(".") + 2, "**/")
        call append(line(".") + 3, "")
    endif
endfunc
