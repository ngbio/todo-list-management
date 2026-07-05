import TodoItem from "./TodoItem";

function TodoList({ todos, pagination, onEdit, onToggle, onDelete, onPageChange }) {
    if (todos.length === 0) {
        return (
            <div className="empty-state">
                <h3>Chưa có công việc phù hợp</h3>
                <p>Hay thêm công việc mới hoặc thay đổi bộ lọc hiện tại.</p>
            </div>
        );
    }

    const pages = Array.from({ length: pagination.pages }, (_, index) => index + 1);

    return (
        <>
            <div className="todo-list">
                {todos.map(todo => (
                    <TodoItem key={todo.id} todo={todo} onEdit={onEdit} onToggle={onToggle} onDelete={onDelete} />
                ))}
            </div>

            {pagination.pages > 1 && (
                <nav className="pagination" aria-label="Phân trang công việc">
                    <button className="page-button" type="button" disabled={!pagination.has_prev} onClick={() => onPageChange(pagination.page - 1)}>
                        Trước
                    </button>
                    {pages.map(page => (
                        <button
                            className={`page-button ${page === pagination.page ? "is-current" : ""}`}
                            type="button"
                            key={page}
                            onClick={() => onPageChange(page)}
                        >
                            {page}
                        </button>
                    ))}
                    <button className="page-button" type="button" disabled={!pagination.has_next} onClick={() => onPageChange(pagination.page + 1)}>
                        Sau
                    </button>
                </nav>
            )}
        </>
    );
}

export default TodoList;
