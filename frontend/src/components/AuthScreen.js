import { useState } from "react";
import { login, register } from "../services/authService";

const initialForm = {
    name: "",
    email: "",
    username: "",
    password: "",
    confirm: "",
};

function AuthScreen({ onAuthenticated }) {
    const [mode, setMode] = useState("login");
    const [form, setForm] = useState(initialForm);
    const [message, setMessage] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    const isRegisterMode = mode === "register";

    const updateField = event => {
        const { name, value } = event.target;
        setForm(current => ({ ...current, [name]: value }));
    };

    const changeMode = nextMode => {
        setMode(nextMode);
        setMessage(null);
        setForm(initialForm);
    };

    const getErrorMessage = error => {
        const data = error.response?.data;
        if (Array.isArray(data?.errors)) {
            return data.errors.join(" ");
        }

        return data?.error || "Không thể thực hiện được yêu cầu. Vui lòng thử lại sau.";
    };

    const handleSubmit = async event => {
        event.preventDefault();
        setSubmitting(true);
        setMessage(null);

        try {
            if (isRegisterMode) {
                await register(form);
                setMode("login");
                setForm(current => ({ ...initialForm, username: current.username }));
                setMessage({ type: "success", text: "Đăng ký thành công. Vui lòng đăng nhập để tiếp tục." });
                return;
            }

            const response = await login({ username: form.username, password: form.password });
            onAuthenticated(response.data.user);
        } catch (error) {
            setMessage({ type: "danger", text: getErrorMessage(error) });
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <section className="auth-layout">
            <div className="auth-copy">
                <p>Todo management</p>
                <h1>Quản lý công việc cá nhân</h1>
                <span>Đăng nhập để lưu, tìm kiếm và đồng bộ danh sách công việc của bạn trên database MySQL.</span>
            </div>

            <form className="panel auth-panel" onSubmit={handleSubmit}>
                <div className="auth-tabs" role="tablist" aria-label="Chọn hình thức xác thực">
                    <button
                        className={mode === "login" ? "active" : ""}
                        type="button"
                        onClick={() => changeMode("login")}
                    >
                        Đăng nhập
                    </button>
                    <button
                        className={mode === "register" ? "active" : ""}
                        type="button"
                        onClick={() => changeMode("register")}
                    >
                        Đăng ký
                    </button>
                </div>

                <h2>{isRegisterMode ? "Tạo tài khoản" : "Chào mừng trở lại"}</h2>

                {message && <div className={`alert ${message.type}`}>{message.text}</div>}

                {isRegisterMode && (
                    <>
                        <div className="field-group">
                            <label htmlFor="name">Họ tên <span>*</span></label>
                            <input id="name" name="name" value={form.name} onChange={updateField} placeholder="Nguyen Van A" />
                        </div>
                        <div className="field-group">
                            <label htmlFor="email">Email <span>*</span></label>
                            <input id="email" name="email" type="email" value={form.email} onChange={updateField} placeholder="you@example.com" />
                        </div>
                    </>
                )}

                <div className="field-group">
                    <label htmlFor="username">Tên đăng nhập <span>*</span></label>
                    <input id="username" name="username" value={form.username} onChange={updateField} placeholder="username" />
                </div>

                <div className="field-group">
                    <label htmlFor="password">Mật khẩu <span>*</span></label>
                    <input id="password" name="password" type="password" value={form.password} onChange={updateField} placeholder="Nhập mật khẩu" />
                </div>

                {isRegisterMode && (
                    <div className="field-group">
                        <label htmlFor="confirm">Nhập lại mật khẩu <span>*</span></label>
                        <input id="confirm" name="confirm" type="password" value={form.confirm} onChange={updateField} placeholder="Nhập lại mật khẩu" />
                    </div>
                )}

                <button className="btn btn-primary auth-submit" type="submit" disabled={submitting}>
                    {submitting ? "Đang xử lý..." : isRegisterMode ? "Đăng ký" : "Đăng nhập"}
                </button>
            </form>
        </section>
    );
}

export default AuthScreen;
