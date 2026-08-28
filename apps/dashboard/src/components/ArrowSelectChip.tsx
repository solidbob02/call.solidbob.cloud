import { useEffect, useId, useRef, useState, type ReactElement } from "react";

export interface ArrowSelectOption<T extends string = string> {
  value: T;
  label: string;
  color?: string;
}

interface ArrowSelectChipProps<T extends string> {
  options: readonly ArrowSelectOption<T>[];
  value: T;
  onChange: (value: T) => void;
  "aria-label"?: string;
}

const closers = new Map<symbol, () => void>();

function closeOthers(self: symbol): void {
  for (const [id, close] of closers) {
    if (id !== self) {
      close();
    }
  }
}

export function ArrowSelectChip<T extends string>({
  options,
  value,
  onChange,
  "aria-label": ariaLabel,
}: ArrowSelectChipProps<T>): ReactElement {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const self = useRef(Symbol("arrow-select"));
  const menuId = useId();
  const selected = options.find((option) => option.value === value);

  useEffect(() => {
    const id = self.current;
    closers.set(id, () => {
      setOpen(false);
    });
    return () => {
      closers.delete(id);
    };
  }, []);

  useEffect(() => {
    if (!open) {
      return;
    }
    function onPointerDown(event: PointerEvent): void {
      const root = rootRef.current;
      if (root !== null && !root.contains(event.target as Node)) {
        setOpen(false);
      }
    }
    function onKeyDown(event: KeyboardEvent): void {
      if (event.key === "Escape") {
        setOpen(false);
      }
    }
    document.addEventListener("pointerdown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("pointerdown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  function toggle(): void {
    if (open) {
      setOpen(false);
      return;
    }
    closeOthers(self.current);
    setOpen(true);
  }

  function pick(next: T): void {
    onChange(next);
    setOpen(false);
  }

  return (
    <div className={`arrow-select${open ? " is-open" : ""}`} ref={rootRef}>
      <button
        type="button"
        className="arrow-select-trigger"
        aria-label={ariaLabel}
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={menuId}
        onClick={toggle}
      >
        {selected?.color !== undefined ? (
          <span
            className="arrow-select-dot"
            style={{ background: selected.color }}
            aria-hidden="true"
          />
        ) : null}
        <span className="arrow-select-label">{selected?.label ?? value}</span>
        <ChevronIcon />
      </button>
      {open ? (
        <ul className="arrow-select-menu" id={menuId} role="listbox">
          {options.map((option) => {
            const active = option.value === value;
            return (
              <li key={option.value} role="presentation">
                <button
                  type="button"
                  className={`arrow-select-option${active ? " is-active" : ""}`}
                  role="option"
                  aria-selected={active}
                  onClick={() => {
                    pick(option.value);
                  }}
                >
                  {option.color !== undefined ? (
                    <span
                      className="arrow-select-dot"
                      style={{ background: option.color }}
                      aria-hidden="true"
                    />
                  ) : null}
                  <span>{option.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      ) : null}
    </div>
  );
}

function ChevronIcon(): ReactElement {
  return (
    <svg
      className="arrow-select-chevron"
      width="12"
      height="12"
      viewBox="0 0 12 12"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M2.4 4.4 6 8l3.6-3.6"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
