import { useEffect, useState } from "react";
import { validateTodo } from "../utils/todoValidator";

const initialForm = { title: "", description: "" };

function TodoForm({ editingTodo, onSubmit, onCancel, submitting }) {
    const [form, setForm] = useState(initialForm);
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (editingTodo) {
            setForm({
                title: editingTodo.title || "",
                description: editingTodo.description || "",
            });
            setErrors({});
        } else {
            setForm(initialForm);
        }
    }, [editingTodo]);

    const updateField = event => {
        const { name, value } = event.target;
        setForm(current => ({ ...current, [name]: value }));
    };

    const handleSubmit = event => {
        event.preventDefault();
        const validationErrors = validateTodo(form);
        setErrors(validationErrors);

        if (Object.keys(validationErrors).length > 0) {
            return;
        }

        onSubmit({
            title: form.title.trim(),
            description: form.description.trim(),
        });

        if (!editingTodo) {
            setForm(initialForm);
        }
    };

    return (
        <section className="panel">
            <h2>{editingTodo ? "Chỉnh sửa công việc" : "Thêm công việc mới"}</h2>
            <form onSubmit={handleSubmit} noValidate>
                <div className="field-group">
                    <label htmlFor="title">Tiêu đề <span>*</span></label>
                    <input
                        id="title"
                        type="text"
                        name="title"
                        value={form.title}
                        maxLength={120}
                        placeholder="VD: Hoàn thành báo cáo tuần"
                        className={errors.title ? "is-invalid" : ""}
                        onChange={updateField}
                    />
                    {errors.title && <small className="field-error">{errors.title}</small>}
                </div>

                <div className="field-group">
                    <label htmlFor="description">Mô tả</label>
                    <textarea
                        id="description"
                        name="description"
                        value={form.description}
                        rows={5}
                        maxLength={1000}
                        placeholder="Ghi chú thêm nếu cần"
                        className={errors.description ? "is-invalid" : ""}
                        onChange={updateField}
                    />
                    {errors.description && <small className="field-error">{errors.description}</small>}
                </div>

                <div className="button-row">
                    <button className="btn btn-primary" type="submit" disabled={submitting}>
                        {editingTodo ? "Lưu thay đổi" : "Thêm công việc"}
                    </button>
                    {editingTodo && (
                        <button className="btn btn-secondary" type="button" onClick={onCancel}>
                            Hủy
                        </button>
                    )}
                </div>
            </form>
        </section>
    );
}

export default TodoForm;
