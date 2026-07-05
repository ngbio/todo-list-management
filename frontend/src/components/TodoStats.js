function TodoStats({ stats }) {
    const items = [
        { label: "Tổng công việc", value: stats.total || 0 },
        { label: "Chưa xong", value: stats.active || 0 },
        { label: "Hoàn thành", value: stats.completed || 0 },
    ];

    return (
        <section className="stats-grid">
            {items.map(item => (
                <div className="stat-card" key={item.label}>
                    <span>{item.label}</span>
                    <strong>{item.value}</strong>
                </div>
            ))}
        </section>
    );
}

export default TodoStats;
