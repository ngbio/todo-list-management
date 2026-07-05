import { useCallback, useEffect, useState } from "react";
import MySpinner from "../../components/MySpinner";
import TodoFilters from "../../components/TodoFilters";
import TodoForm from "../../components/TodoForm";
import TodoList from "../../components/TodoList";
import TodoStats from "../../components/TodoStats";
import { createTodo, deleteTodo, getTodos, toggleTodo, updateTodo } from "../../services/todoService";

const defaultFilters = {
    keyword: "",
    status: "all",
    sort: "newest",
    page: 1,
    per_page: 8,
};

const defaultPagination = {
    page: 1,
    pages: 1,
    total: 0,
    has_next: false,
    has_prev: false,
};

function Home({ onUnauthorized }) {
    const [todos, setTodos] = useState([]);
    const [stats, setStats] = useState({ total: 0, active: 0, completed: 0 });
    const [filters, setFilters] = useState(defaultFilters);
    const [pagination, setPagination] = useState(defaultPagination);
    const [editingTodo, setEditingTodo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState(null);

    const isUnauthorized = error => error.response?.status === 401;

    const handleUnauthorized = useCallback(() => {
        setMessage({ type: "danger", text: "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại." });
        onUnauthorized?.();
    }, [onUnauthorized]);

    const loadTodos = useCallback(async () => {
        setLoading(true);
        try {
            const response = await getTodos(filters);
            setTodos(response.data.items || []);
            setStats(response.data.stats || { total: 0, active: 0, completed: 0 });
            setPagination({
                page: response.data.page,
                pages: response.data.pages,
                total: response.data.total,
                has_next: response.data.has_next,
                has_prev: response.data.has_prev,
            });
        } catch (error) {
            if (isUnauthorized(error)) {
                handleUnauthorized();
                return;
            }

            setMessage({ type: "danger", text: "Không tải được danh sách công việc." });
        } finally {
            setLoading(false);
        }
    }, [filters, handleUnauthorized]);

    useEffect(() => {
        loadTodos();
    }, [loadTodos]);

    const handleSubmit = async payload => {
        setSubmitting(true);
        try {
            if (editingTodo) {
                await updateTodo(editingTodo.id, payload);
                setMessage({ type: "success", text: "Đã cập nhật công việc." });
            } else {
                await createTodo(payload);
                setMessage({ type: "success", text: "Đã thêm công việc mới." });
            }

            setEditingTodo(null);
            setFilters(current => ({ ...current, page: 1 }));
            await loadTodos();
        } catch (error) {
            if (isUnauthorized(error)) {
                handleUnauthorized();
                return;
            }

            const errors = error.response?.data?.errors;
            setMessage({ type: "danger", text: errors ? errors.join(" ") : "Không lưu được công việc." });
        } finally {
            setSubmitting(false);
        }
    };

    const handleToggle = async id => {
        try {
            await toggleTodo(id);
            await loadTodos();
        } catch (error) {
            if (isUnauthorized(error)) {
                handleUnauthorized();
                return;
            }

            setMessage({ type: "danger", text: "Không cập nhật được trạng thái công việc." });
        }
    };

    const handleDelete = async id => {
        if (!window.confirm("Bạn chắc chắn muốn xóa công việc này?")) {
            return;
        }

        try {
            await deleteTodo(id);
            setMessage({ type: "success", text: "Đã xóa công việc." });
            await loadTodos();
        } catch (error) {
            if (isUnauthorized(error)) {
                handleUnauthorized();
                return;
            }

            setMessage({ type: "danger", text: "Không xóa được công việc." });
        }
    };

    const submitFilters = event => {
        event.preventDefault();
        setFilters(current => ({ ...current, page: 1 }));
    };

    return (
        <>
            <section className="page-heading">
                <p>Todo management</p>
                <h1>Quản lý công việc</h1>
                <span>Thêm, sửa, xóa, tìm kiếm và theo dõi trạng thái công việc với ReactJS.</span>
            </section>

            {message && (
                <div className={`alert ${message.type}`}>
                    <span>{message.text}</span>
                    <button type="button" onClick={() => setMessage(null)}>Đóng</button>
                </div>
            )}

            <TodoStats stats={stats} />

            <div className="workspace-grid">
                <TodoForm editingTodo={editingTodo} onSubmit={handleSubmit} onCancel={() => setEditingTodo(null)} submitting={submitting} />
                <section>
                    <TodoFilters filters={filters} onChange={setFilters} onSubmit={submitFilters} />
                    {loading ? <MySpinner /> : (
                        <TodoList
                            todos={todos}
                            pagination={pagination}
                            onEdit={setEditingTodo}
                            onToggle={handleToggle}
                            onDelete={handleDelete}
                            onPageChange={page => setFilters(current => ({ ...current, page }))}
                        />
                    )}
                </section>
            </div>
        </>
    );
}

export default Home;
