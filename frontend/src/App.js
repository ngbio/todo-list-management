import { useEffect, useState } from "react";
import AuthScreen from "./components/AuthScreen";
import Footer from "./components/Footer";
import Header from "./components/Header";
import MySpinner from "./components/MySpinner";
import Home from "./screens/home/Home";
import { getProfile, logout } from "./services/authService";

function App() {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme === "light" || savedTheme === "dark" ? savedTheme : "light";
  });
  const [user, setUser] = useState(null);
  const [checkingSession, setCheckingSession] = useState(true);

  useEffect(() => {
    document.body.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await getProfile();
        setUser(response.data.user);
      } catch (error) {
        setUser(null);
      } finally {
        setCheckingSession(false);
      }
    };

    loadProfile();
  }, []);

  const toggleTheme = () => {
    setTheme(currentTheme => currentTheme === "dark" ? "light" : "dark");
  };

  const handleLogout = async () => {
    try {
      await logout();
    } finally {
      setUser(null);
    }
  };

  return (
    <>
      <Header theme={theme} onToggleTheme={toggleTheme} user={user} onLogout={handleLogout} />
      <main className="container main-container">
        {checkingSession ? (
          <div className="session-loading">
            <MySpinner />
          </div>
        ) : user ? (
          <Home onUnauthorized={() => setUser(null)} />
        ) : (
          <AuthScreen onAuthenticated={setUser} />
        )}
      </main>
      <Footer />
    </>
  );
}

export default App;
