function Header({ theme, onToggleTheme, user, onLogout }) {
    return (
        <header className="app-header">
            <div className="container header-inner">
                <a className="brand" href="/">Todo List</a>
                <div className="header-actions">
                    {user ? (
                        <span className="user-chip">{user.name || user.username}</span>
                    ) : (
                        <span className="header-subtitle">ReactJS + Flask API</span>
                    )}
                    <button className="btn btn-ghost" type="button" onClick={onToggleTheme}>
                        {theme === "dark" ? "Light" : "Dark"}
                    </button>
                    {user && (
                        <button className="btn btn-secondary" type="button" onClick={onLogout}>
                            Đăng xuất
                        </button>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Header;
