<%inherit file='base.mako' />

% if user:
<p>You are logged in as: <a href="${ request.route_url('user', login=user.login) }">${ user.login }</a></p>
<p><a href="${ request.route_url('logout') }">Logout</a></p>
% else:
<p>You are not logged in!</p>
<p><a href="${ request.route_url('login') }">Login</a></p>
% endif

<p>Upload a file <a href="${ request.route_url('file.upload') }">here</a></p>

<p><a href="${ request.route_url('file.list') }">All files</a></p>
<p><a href="${ request.route_url('users') }">All Users</a></p>

<h2>Your files</h2>
% if user_files:
% for file in user_files:
<p>
    <a href="${ request.route_url('file.show', title=file.uri) }">${ file.title }</a>
</p>
% endfor
% else:
<p>You have not upload any files.</p>
% endif
