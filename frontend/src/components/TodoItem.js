function TodoItem({ todo, onEdit, onToggle, onDelete }) {
    const createdAt = todo.created_at ? new Date(todo.created_at).toLocaleString("vi-VN") : "";

    return (
        <article className={`todo-item ${todo.is_completed ? "is-completed" : ""}`}>
            <div className="todo-main">
                <button className="status-toggle" type="button" aria-label="Đổi trạng thái" onClick={() => onToggle(todo.id)}>
                    {todo.is_completed ? "✓" : ""}
                </button>

                <div className="todo-content">
                    <div className="todo-title-row">
                        <h3>{todo.title}</h3>
                        <span className={`status-badge ${todo.is_completed ? "done" : "active"}`}>
                            {todo.is_completed ? "Hoàn thành" : "Chưa xong"}
                        </span>
                    </div>
                    {todo.description && <p>{todo.description}</p>}
                    {createdAt && <small>Tạo lúc {createdAt}</small>}
                </div>
            </div>

            <div className="todo-actions">
                <button className="btn btn-secondary" type="button" onClick={() => onEdit(todo)}>Chỉnh sửa</button>
                <button className="btn btn-danger" type="button" onClick={() => onDelete(todo.id)}>Xóa</button>
            </div>
        </article>
    );
}

export default TodoItem;
