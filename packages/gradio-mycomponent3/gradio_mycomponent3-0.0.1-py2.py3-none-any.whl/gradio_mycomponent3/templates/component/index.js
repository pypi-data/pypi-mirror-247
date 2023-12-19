const {
  SvelteComponent: Jt,
  assign: Qt,
  create_slot: xt,
  detach: $t,
  element: el,
  get_all_dirty_from_scope: tl,
  get_slot_changes: ll,
  get_spread_update: nl,
  init: il,
  insert: sl,
  safe_not_equal: ol,
  set_dynamic_element_data: xe,
  set_style: B,
  toggle_class: $,
  transition_in: Et,
  transition_out: Bt,
  update_slot_base: fl
} = window.__gradio__svelte__internal;
function al(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), s = xt(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-1t38q2d"
    }
  ], f = {};
  for (let a = 0; a < o.length; a += 1)
    f = Qt(f, o[a]);
  return {
    c() {
      e = el(
        /*tag*/
        l[14]
      ), s && s.c(), xe(
        /*tag*/
        l[14]
      )(e, f), $(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), $(
        e,
        "padded",
        /*padding*/
        l[6]
      ), $(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), $(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), B(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), B(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), B(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), B(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), B(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), B(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), B(e, "border-width", "var(--block-border-width)");
    },
    m(a, _) {
      sl(a, e, _), s && s.m(e, null), n = !0;
    },
    p(a, _) {
      s && s.p && (!n || _ & /*$$scope*/
      131072) && fl(
        s,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? ll(
          i,
          /*$$scope*/
          a[17],
          _,
          null
        ) : tl(
          /*$$scope*/
          a[17]
        ),
        null
      ), xe(
        /*tag*/
        a[14]
      )(e, f = nl(o, [
        (!n || _ & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!n || _ & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!n || _ & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-1t38q2d")) && { class: t }
      ])), $(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), $(
        e,
        "padded",
        /*padding*/
        a[6]
      ), $(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), $(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), _ & /*height*/
      1 && B(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), _ & /*width*/
      2 && B(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), _ & /*variant*/
      16 && B(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), _ & /*allow_overflow*/
      2048 && B(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && B(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), _ & /*min_width*/
      8192 && B(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (Et(s, a), n = !0);
    },
    o(a) {
      Bt(s, a), n = !1;
    },
    d(a) {
      a && $t(e), s && s.d(a);
    }
  };
}
function _l(l) {
  let e, t = (
    /*tag*/
    l[14] && al(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (Et(t, n), e = !0);
    },
    o(n) {
      Bt(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function rl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: o = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: _ = "solid" } = e, { border_mode: r = "base" } = e, { padding: u = !0 } = e, { type: m = "normal" } = e, { test_id: w = void 0 } = e, { explicit_call: q = !1 } = e, { container: M = !0 } = e, { visible: S = !0 } = e, { allow_overflow: z = !0 } = e, { scale: F = null } = e, { min_width: d = 0 } = e, y = m === "fieldset" ? "fieldset" : "div";
  const N = (h) => {
    if (h !== void 0) {
      if (typeof h == "number")
        return h + "px";
      if (typeof h == "string")
        return h;
    }
  };
  return l.$$set = (h) => {
    "height" in h && t(0, s = h.height), "width" in h && t(1, o = h.width), "elem_id" in h && t(2, f = h.elem_id), "elem_classes" in h && t(3, a = h.elem_classes), "variant" in h && t(4, _ = h.variant), "border_mode" in h && t(5, r = h.border_mode), "padding" in h && t(6, u = h.padding), "type" in h && t(16, m = h.type), "test_id" in h && t(7, w = h.test_id), "explicit_call" in h && t(8, q = h.explicit_call), "container" in h && t(9, M = h.container), "visible" in h && t(10, S = h.visible), "allow_overflow" in h && t(11, z = h.allow_overflow), "scale" in h && t(12, F = h.scale), "min_width" in h && t(13, d = h.min_width), "$$scope" in h && t(17, i = h.$$scope);
  }, [
    s,
    o,
    f,
    a,
    _,
    r,
    u,
    w,
    q,
    M,
    S,
    z,
    F,
    d,
    y,
    N,
    m,
    i,
    n
  ];
}
class ul extends Jt {
  constructor(e) {
    super(), il(this, e, rl, _l, ol, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: cl,
  attr: dl,
  create_slot: ml,
  detach: bl,
  element: hl,
  get_all_dirty_from_scope: gl,
  get_slot_changes: wl,
  init: pl,
  insert: kl,
  safe_not_equal: vl,
  transition_in: yl,
  transition_out: ql,
  update_slot_base: Cl
} = window.__gradio__svelte__internal;
function Sl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = ml(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = hl("div"), i && i.c(), dl(e, "class", "svelte-1hnfib2");
    },
    m(s, o) {
      kl(s, e, o), i && i.m(e, null), t = !0;
    },
    p(s, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && Cl(
        i,
        n,
        s,
        /*$$scope*/
        s[0],
        t ? wl(
          n,
          /*$$scope*/
          s[0],
          o,
          null
        ) : gl(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (yl(i, s), t = !0);
    },
    o(s) {
      ql(i, s), t = !1;
    },
    d(s) {
      s && bl(e), i && i.d(s);
    }
  };
}
function Fl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, n];
}
class Ll extends cl {
  constructor(e) {
    super(), pl(this, e, Fl, Sl, vl, {});
  }
}
const {
  SvelteComponent: Tl,
  attr: $e,
  check_outros: Vl,
  create_component: zl,
  create_slot: Ml,
  destroy_component: Nl,
  detach: Te,
  element: El,
  empty: Bl,
  get_all_dirty_from_scope: Hl,
  get_slot_changes: Zl,
  group_outros: Pl,
  init: jl,
  insert: Ve,
  mount_component: Dl,
  safe_not_equal: Al,
  set_data: Il,
  space: Ul,
  text: Yl,
  toggle_class: ue,
  transition_in: ve,
  transition_out: ze,
  update_slot_base: Kl
} = window.__gradio__svelte__internal;
function et(l) {
  let e, t;
  return e = new Ll({
    props: {
      $$slots: { default: [Xl] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      zl(e.$$.fragment);
    },
    m(n, i) {
      Dl(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (ve(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ze(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Nl(e, n);
    }
  };
}
function Xl(l) {
  let e;
  return {
    c() {
      e = Yl(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Ve(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Il(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Te(e);
    }
  };
}
function Gl(l) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    l[2].default
  ), o = Ml(
    s,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let f = (
    /*info*/
    l[1] && et(l)
  );
  return {
    c() {
      e = El("span"), o && o.c(), t = Ul(), f && f.c(), n = Bl(), $e(e, "data-testid", "block-info"), $e(e, "class", "svelte-22c38v"), ue(e, "sr-only", !/*show_label*/
      l[0]), ue(e, "hide", !/*show_label*/
      l[0]), ue(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(a, _) {
      Ve(a, e, _), o && o.m(e, null), Ve(a, t, _), f && f.m(a, _), Ve(a, n, _), i = !0;
    },
    p(a, [_]) {
      o && o.p && (!i || _ & /*$$scope*/
      8) && Kl(
        o,
        s,
        a,
        /*$$scope*/
        a[3],
        i ? Zl(
          s,
          /*$$scope*/
          a[3],
          _,
          null
        ) : Hl(
          /*$$scope*/
          a[3]
        ),
        null
      ), (!i || _ & /*show_label*/
      1) && ue(e, "sr-only", !/*show_label*/
      a[0]), (!i || _ & /*show_label*/
      1) && ue(e, "hide", !/*show_label*/
      a[0]), (!i || _ & /*info*/
      2) && ue(
        e,
        "has-info",
        /*info*/
        a[1] != null
      ), /*info*/
      a[1] ? f ? (f.p(a, _), _ & /*info*/
      2 && ve(f, 1)) : (f = et(a), f.c(), ve(f, 1), f.m(n.parentNode, n)) : f && (Pl(), ze(f, 1, 1, () => {
        f = null;
      }), Vl());
    },
    i(a) {
      i || (ve(o, a), ve(f), i = !0);
    },
    o(a) {
      ze(o, a), ze(f), i = !1;
    },
    d(a) {
      a && (Te(e), Te(t), Te(n)), o && o.d(a), f && f.d(a);
    }
  };
}
function Ol(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: o = void 0 } = e;
  return l.$$set = (f) => {
    "show_label" in f && t(0, s = f.show_label), "info" in f && t(1, o = f.info), "$$scope" in f && t(3, i = f.$$scope);
  }, [s, o, n, i];
}
class Rl extends Tl {
  constructor(e) {
    super(), jl(this, e, Ol, Gl, Al, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Wl,
  append: Jl,
  attr: ee,
  detach: Ql,
  init: xl,
  insert: $l,
  noop: je,
  safe_not_equal: en,
  svg_element: tt
} = window.__gradio__svelte__internal;
function tn(l) {
  let e, t;
  return {
    c() {
      e = tt("svg"), t = tt("polyline"), ee(t, "points", "20 6 9 17 4 12"), ee(e, "xmlns", "http://www.w3.org/2000/svg"), ee(e, "viewBox", "2 0 20 20"), ee(e, "fill", "none"), ee(e, "stroke", "currentColor"), ee(e, "stroke-width", "3"), ee(e, "stroke-linecap", "round"), ee(e, "stroke-linejoin", "round");
    },
    m(n, i) {
      $l(n, e, i), Jl(e, t);
    },
    p: je,
    i: je,
    o: je,
    d(n) {
      n && Ql(e);
    }
  };
}
class ln extends Wl {
  constructor(e) {
    super(), xl(this, e, null, tn, en, {});
  }
}
const {
  SvelteComponent: nn,
  append: lt,
  attr: se,
  detach: sn,
  init: on,
  insert: fn,
  noop: De,
  safe_not_equal: an,
  svg_element: Ae
} = window.__gradio__svelte__internal;
function _n(l) {
  let e, t, n;
  return {
    c() {
      e = Ae("svg"), t = Ae("path"), n = Ae("path"), se(t, "fill", "currentColor"), se(t, "d", "M28 10v18H10V10h18m0-2H10a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2Z"), se(n, "fill", "currentColor"), se(n, "d", "M4 18H2V4a2 2 0 0 1 2-2h14v2H4Z"), se(e, "xmlns", "http://www.w3.org/2000/svg"), se(e, "viewBox", "0 0 33 33"), se(e, "color", "currentColor");
    },
    m(i, s) {
      fn(i, e, s), lt(e, t), lt(e, n);
    },
    p: De,
    i: De,
    o: De,
    d(i) {
      i && sn(e);
    }
  };
}
class rn extends nn {
  constructor(e) {
    super(), on(this, e, null, _n, an, {});
  }
}
const un = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], nt = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
un.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: nt[e][t],
      secondary: nt[e][n]
    }
  }),
  {}
);
function Me() {
}
const cn = (l) => l;
function dn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Ht = typeof window < "u";
let it = Ht ? () => window.performance.now() : () => Date.now(), Zt = Ht ? (l) => requestAnimationFrame(l) : Me;
const he = /* @__PURE__ */ new Set();
function Pt(l) {
  he.forEach((e) => {
    e.c(l) || (he.delete(e), e.f());
  }), he.size !== 0 && Zt(Pt);
}
function mn(l) {
  let e;
  return he.size === 0 && Zt(Pt), {
    promise: new Promise((t) => {
      he.add(e = { c: l, f: t });
    }),
    abort() {
      he.delete(e);
    }
  };
}
function bn(l, { delay: e = 0, duration: t = 400, easing: n = cn } = {}) {
  const i = +getComputedStyle(l).opacity;
  return {
    delay: e,
    duration: t,
    easing: n,
    css: (s) => `opacity: ${s * i}`
  };
}
const ce = [];
function hn(l, e = Me) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (dn(l, f) && (l = f, t)) {
      const a = !ce.length;
      for (const _ of n)
        _[1](), ce.push(_, l);
      if (a) {
        for (let _ = 0; _ < ce.length; _ += 2)
          ce[_][0](ce[_ + 1]);
        ce.length = 0;
      }
    }
  }
  function s(f) {
    i(f(l));
  }
  function o(f, a = Me) {
    const _ = [f, a];
    return n.add(_), n.size === 1 && (t = e(i, s) || Me), f(l), () => {
      n.delete(_), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: o };
}
function st(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ue(l, e, t, n) {
  if (typeof t == "number" || st(t)) {
    const i = n - t, s = (t - e) / (l.dt || 1 / 60), o = l.opts.stiffness * i, f = l.opts.damping * s, a = (o - f) * l.inv_mass, _ = (s + a) * l.dt;
    return Math.abs(_) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, st(t) ? new Date(t.getTime() + _) : t + _);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => Ue(l, e[s], t[s], n[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = Ue(l, e[s], t[s], n[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function ot(l, e = {}) {
  const t = hn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let o, f, a, _ = l, r = l, u = 1, m = 0, w = !1;
  function q(S, z = {}) {
    r = S;
    const F = a = {};
    return l == null || z.hard || M.stiffness >= 1 && M.damping >= 1 ? (w = !0, o = it(), _ = S, t.set(l = r), Promise.resolve()) : (z.soft && (m = 1 / ((z.soft === !0 ? 0.5 : +z.soft) * 60), u = 0), f || (o = it(), w = !1, f = mn((d) => {
      if (w)
        return w = !1, f = null, !1;
      u = Math.min(u + m, 1);
      const y = {
        inv_mass: u,
        opts: M,
        settled: !0,
        dt: (d - o) * 60 / 1e3
      }, N = Ue(y, _, l, r);
      return o = d, _ = l, t.set(l = N), y.settled && (f = null), !y.settled;
    })), new Promise((d) => {
      f.promise.then(() => {
        F === a && d();
      });
    }));
  }
  const M = {
    set: q,
    update: (S, z) => q(S(r, l), z),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: s
  };
  return M;
}
const {
  SvelteComponent: gn,
  action_destroyer: wn,
  add_render_callback: pn,
  append: kn,
  attr: v,
  binding_callbacks: Se,
  bubble: te,
  check_outros: Ke,
  create_component: Xe,
  create_in_transition: vn,
  destroy_component: Ge,
  detach: U,
  element: fe,
  empty: jt,
  group_outros: Oe,
  init: yn,
  insert: Y,
  is_function: qn,
  listen: V,
  mount_component: Re,
  noop: Ne,
  run_all: Be,
  safe_not_equal: Cn,
  set_data: Sn,
  set_input_value: ne,
  space: Dt,
  text: Fn,
  toggle_class: ft,
  transition_in: R,
  transition_out: x
} = window.__gradio__svelte__internal, { beforeUpdate: Ln, afterUpdate: Tn, createEventDispatcher: Vn, tick: at } = window.__gradio__svelte__internal;
function zn(l) {
  let e;
  return {
    c() {
      e = Fn(
        /*label*/
        l[3]
      );
    },
    m(t, n) {
      Y(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      8 && Sn(
        e,
        /*label*/
        t[3]
      );
    },
    d(t) {
      t && U(e);
    }
  };
}
function Mn(l) {
  let e, t, n, i, s, o, f, a, _ = (
    /*show_label*/
    l[6] && /*show_copy_button*/
    l[10] && _t(l)
  );
  return {
    c() {
      _ && _.c(), e = Dt(), t = fe("textarea"), v(t, "data-testid", "textbox"), v(t, "class", "scroll-hide svelte-18tqgac"), v(t, "dir", n = /*rtl*/
      l[11] ? "rtl" : "ltr"), v(
        t,
        "placeholder",
        /*placeholder*/
        l[2]
      ), v(
        t,
        "rows",
        /*lines*/
        l[1]
      ), t.disabled = /*disabled*/
      l[5], t.autofocus = /*autofocus*/
      l[12], v(t, "style", i = /*text_align*/
      l[13] ? "text-align: " + /*text_align*/
      l[13] : "");
    },
    m(r, u) {
      _ && _.m(r, u), Y(r, e, u), Y(r, t, u), ne(
        t,
        /*value*/
        l[0]
      ), l[38](t), o = !0, /*autofocus*/
      l[12] && t.focus(), f || (a = [
        wn(s = /*text_area_resize*/
        l[20].call(
          null,
          t,
          /*value*/
          l[0]
        )),
        V(
          t,
          "input",
          /*textarea_input_handler*/
          l[37]
        ),
        V(
          t,
          "keypress",
          /*handle_keypress*/
          l[18]
        ),
        V(
          t,
          "blur",
          /*blur_handler_3*/
          l[29]
        ),
        V(
          t,
          "select",
          /*handle_select*/
          l[17]
        ),
        V(
          t,
          "focus",
          /*focus_handler_3*/
          l[30]
        ),
        V(
          t,
          "scroll",
          /*handle_scroll*/
          l[19]
        )
      ], f = !0);
    },
    p(r, u) {
      /*show_label*/
      r[6] && /*show_copy_button*/
      r[10] ? _ ? (_.p(r, u), u[0] & /*show_label, show_copy_button*/
      1088 && R(_, 1)) : (_ = _t(r), _.c(), R(_, 1), _.m(e.parentNode, e)) : _ && (Oe(), x(_, 1, 1, () => {
        _ = null;
      }), Ke()), (!o || u[0] & /*rtl*/
      2048 && n !== (n = /*rtl*/
      r[11] ? "rtl" : "ltr")) && v(t, "dir", n), (!o || u[0] & /*placeholder*/
      4) && v(
        t,
        "placeholder",
        /*placeholder*/
        r[2]
      ), (!o || u[0] & /*lines*/
      2) && v(
        t,
        "rows",
        /*lines*/
        r[1]
      ), (!o || u[0] & /*disabled*/
      32) && (t.disabled = /*disabled*/
      r[5]), (!o || u[0] & /*autofocus*/
      4096) && (t.autofocus = /*autofocus*/
      r[12]), (!o || u[0] & /*text_align*/
      8192 && i !== (i = /*text_align*/
      r[13] ? "text-align: " + /*text_align*/
      r[13] : "")) && v(t, "style", i), s && qn(s.update) && u[0] & /*value*/
      1 && s.update.call(
        null,
        /*value*/
        r[0]
      ), u[0] & /*value*/
      1 && ne(
        t,
        /*value*/
        r[0]
      );
    },
    i(r) {
      o || (R(_), o = !0);
    },
    o(r) {
      x(_), o = !1;
    },
    d(r) {
      r && (U(e), U(t)), _ && _.d(r), l[38](null), f = !1, Be(a);
    }
  };
}
function Nn(l) {
  let e;
  function t(s, o) {
    if (
      /*type*/
      s[9] === "text"
    )
      return Pn;
    if (
      /*type*/
      s[9] === "password"
    )
      return Zn;
    if (
      /*type*/
      s[9] === "email"
    )
      return Hn;
  }
  let n = t(l), i = n && n(l);
  return {
    c() {
      i && i.c(), e = jt();
    },
    m(s, o) {
      i && i.m(s, o), Y(s, e, o);
    },
    p(s, o) {
      n === (n = t(s)) && i ? i.p(s, o) : (i && i.d(1), i = n && n(s), i && (i.c(), i.m(e.parentNode, e)));
    },
    i: Ne,
    o: Ne,
    d(s) {
      s && U(e), i && i.d(s);
    }
  };
}
function _t(l) {
  let e, t, n, i;
  const s = [Bn, En], o = [];
  function f(a, _) {
    return (
      /*copied*/
      a[15] ? 0 : 1
    );
  }
  return e = f(l), t = o[e] = s[e](l), {
    c() {
      t.c(), n = jt();
    },
    m(a, _) {
      o[e].m(a, _), Y(a, n, _), i = !0;
    },
    p(a, _) {
      let r = e;
      e = f(a), e === r ? o[e].p(a, _) : (Oe(), x(o[r], 1, 1, () => {
        o[r] = null;
      }), Ke(), t = o[e], t ? t.p(a, _) : (t = o[e] = s[e](a), t.c()), R(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (R(t), i = !0);
    },
    o(a) {
      x(t), i = !1;
    },
    d(a) {
      a && U(n), o[e].d(a);
    }
  };
}
function En(l) {
  let e, t, n, i, s;
  return t = new rn({}), {
    c() {
      e = fe("button"), Xe(t.$$.fragment), v(e, "aria-label", "Copy"), v(e, "aria-roledescription", "Copy text"), v(e, "class", "svelte-18tqgac");
    },
    m(o, f) {
      Y(o, e, f), Re(t, e, null), n = !0, i || (s = V(
        e,
        "click",
        /*handle_copy*/
        l[16]
      ), i = !0);
    },
    p: Ne,
    i(o) {
      n || (R(t.$$.fragment, o), n = !0);
    },
    o(o) {
      x(t.$$.fragment, o), n = !1;
    },
    d(o) {
      o && U(e), Ge(t), i = !1, s();
    }
  };
}
function Bn(l) {
  let e, t, n, i;
  return t = new ln({}), {
    c() {
      e = fe("button"), Xe(t.$$.fragment), v(e, "aria-label", "Copied"), v(e, "aria-roledescription", "Text copied"), v(e, "class", "svelte-18tqgac");
    },
    m(s, o) {
      Y(s, e, o), Re(t, e, null), i = !0;
    },
    p: Ne,
    i(s) {
      i || (R(t.$$.fragment, s), s && (n || pn(() => {
        n = vn(e, bn, { duration: 300 }), n.start();
      })), i = !0);
    },
    o(s) {
      x(t.$$.fragment, s), i = !1;
    },
    d(s) {
      s && U(e), Ge(t);
    }
  };
}
function Hn(l) {
  let e, t, n;
  return {
    c() {
      e = fe("input"), v(e, "data-testid", "textbox"), v(e, "type", "email"), v(e, "class", "scroll-hide svelte-18tqgac"), v(
        e,
        "placeholder",
        /*placeholder*/
        l[2]
      ), e.disabled = /*disabled*/
      l[5], e.autofocus = /*autofocus*/
      l[12], v(e, "autocomplete", "email");
    },
    m(i, s) {
      Y(i, e, s), ne(
        e,
        /*value*/
        l[0]
      ), l[36](e), /*autofocus*/
      l[12] && e.focus(), t || (n = [
        V(
          e,
          "input",
          /*input_input_handler_2*/
          l[35]
        ),
        V(
          e,
          "keypress",
          /*handle_keypress*/
          l[18]
        ),
        V(
          e,
          "blur",
          /*blur_handler_2*/
          l[27]
        ),
        V(
          e,
          "select",
          /*handle_select*/
          l[17]
        ),
        V(
          e,
          "focus",
          /*focus_handler_2*/
          l[28]
        )
      ], t = !0);
    },
    p(i, s) {
      s[0] & /*placeholder*/
      4 && v(
        e,
        "placeholder",
        /*placeholder*/
        i[2]
      ), s[0] & /*disabled*/
      32 && (e.disabled = /*disabled*/
      i[5]), s[0] & /*autofocus*/
      4096 && (e.autofocus = /*autofocus*/
      i[12]), s[0] & /*value*/
      1 && e.value !== /*value*/
      i[0] && ne(
        e,
        /*value*/
        i[0]
      );
    },
    d(i) {
      i && U(e), l[36](null), t = !1, Be(n);
    }
  };
}
function Zn(l) {
  let e, t, n;
  return {
    c() {
      e = fe("input"), v(e, "data-testid", "password"), v(e, "type", "password"), v(e, "class", "scroll-hide svelte-18tqgac"), v(
        e,
        "placeholder",
        /*placeholder*/
        l[2]
      ), e.disabled = /*disabled*/
      l[5], e.autofocus = /*autofocus*/
      l[12], v(e, "autocomplete", "");
    },
    m(i, s) {
      Y(i, e, s), ne(
        e,
        /*value*/
        l[0]
      ), l[34](e), /*autofocus*/
      l[12] && e.focus(), t || (n = [
        V(
          e,
          "input",
          /*input_input_handler_1*/
          l[33]
        ),
        V(
          e,
          "keypress",
          /*handle_keypress*/
          l[18]
        ),
        V(
          e,
          "blur",
          /*blur_handler_1*/
          l[25]
        ),
        V(
          e,
          "select",
          /*handle_select*/
          l[17]
        ),
        V(
          e,
          "focus",
          /*focus_handler_1*/
          l[26]
        )
      ], t = !0);
    },
    p(i, s) {
      s[0] & /*placeholder*/
      4 && v(
        e,
        "placeholder",
        /*placeholder*/
        i[2]
      ), s[0] & /*disabled*/
      32 && (e.disabled = /*disabled*/
      i[5]), s[0] & /*autofocus*/
      4096 && (e.autofocus = /*autofocus*/
      i[12]), s[0] & /*value*/
      1 && e.value !== /*value*/
      i[0] && ne(
        e,
        /*value*/
        i[0]
      );
    },
    d(i) {
      i && U(e), l[34](null), t = !1, Be(n);
    }
  };
}
function Pn(l) {
  let e, t, n, i, s;
  return {
    c() {
      e = fe("input"), v(e, "data-testid", "textbox"), v(e, "type", "text"), v(e, "class", "scroll-hide svelte-18tqgac"), v(e, "dir", t = /*rtl*/
      l[11] ? "rtl" : "ltr"), v(
        e,
        "placeholder",
        /*placeholder*/
        l[2]
      ), e.disabled = /*disabled*/
      l[5], e.autofocus = /*autofocus*/
      l[12], v(e, "style", n = /*text_align*/
      l[13] ? "text-align: " + /*text_align*/
      l[13] : "");
    },
    m(o, f) {
      Y(o, e, f), ne(
        e,
        /*value*/
        l[0]
      ), l[32](e), /*autofocus*/
      l[12] && e.focus(), i || (s = [
        V(
          e,
          "input",
          /*input_input_handler*/
          l[31]
        ),
        V(
          e,
          "keypress",
          /*handle_keypress*/
          l[18]
        ),
        V(
          e,
          "blur",
          /*blur_handler*/
          l[23]
        ),
        V(
          e,
          "select",
          /*handle_select*/
          l[17]
        ),
        V(
          e,
          "focus",
          /*focus_handler*/
          l[24]
        )
      ], i = !0);
    },
    p(o, f) {
      f[0] & /*rtl*/
      2048 && t !== (t = /*rtl*/
      o[11] ? "rtl" : "ltr") && v(e, "dir", t), f[0] & /*placeholder*/
      4 && v(
        e,
        "placeholder",
        /*placeholder*/
        o[2]
      ), f[0] & /*disabled*/
      32 && (e.disabled = /*disabled*/
      o[5]), f[0] & /*autofocus*/
      4096 && (e.autofocus = /*autofocus*/
      o[12]), f[0] & /*text_align*/
      8192 && n !== (n = /*text_align*/
      o[13] ? "text-align: " + /*text_align*/
      o[13] : "") && v(e, "style", n), f[0] & /*value*/
      1 && e.value !== /*value*/
      o[0] && ne(
        e,
        /*value*/
        o[0]
      );
    },
    d(o) {
      o && U(e), l[32](null), i = !1, Be(s);
    }
  };
}
function jn(l) {
  let e, t, n, i, s, o;
  t = new Rl({
    props: {
      show_label: (
        /*show_label*/
        l[6]
      ),
      info: (
        /*info*/
        l[4]
      ),
      $$slots: { default: [zn] },
      $$scope: { ctx: l }
    }
  });
  const f = [Nn, Mn], a = [];
  function _(r, u) {
    return (
      /*lines*/
      r[1] === 1 && /*max_lines*/
      r[8] === 1 ? 0 : 1
    );
  }
  return i = _(l), s = a[i] = f[i](l), {
    c() {
      e = fe("label"), Xe(t.$$.fragment), n = Dt(), s.c(), v(e, "class", "svelte-18tqgac"), ft(
        e,
        "container",
        /*container*/
        l[7]
      );
    },
    m(r, u) {
      Y(r, e, u), Re(t, e, null), kn(e, n), a[i].m(e, null), o = !0;
    },
    p(r, u) {
      const m = {};
      u[0] & /*show_label*/
      64 && (m.show_label = /*show_label*/
      r[6]), u[0] & /*info*/
      16 && (m.info = /*info*/
      r[4]), u[0] & /*label*/
      8 | u[1] & /*$$scope*/
      131072 && (m.$$scope = { dirty: u, ctx: r }), t.$set(m);
      let w = i;
      i = _(r), i === w ? a[i].p(r, u) : (Oe(), x(a[w], 1, 1, () => {
        a[w] = null;
      }), Ke(), s = a[i], s ? s.p(r, u) : (s = a[i] = f[i](r), s.c()), R(s, 1), s.m(e, null)), (!o || u[0] & /*container*/
      128) && ft(
        e,
        "container",
        /*container*/
        r[7]
      );
    },
    i(r) {
      o || (R(t.$$.fragment, r), R(s), o = !0);
    },
    o(r) {
      x(t.$$.fragment, r), x(s), o = !1;
    },
    d(r) {
      r && U(e), Ge(t), a[i].d();
    }
  };
}
function Dn(l, e, t) {
  console.log("hello world");
  let { value: n = "" } = e, { value_is_output: i = !1 } = e, { lines: s = 1 } = e, { placeholder: o = "Type here..." } = e, { label: f } = e, { info: a = void 0 } = e, { disabled: _ = !1 } = e, { show_label: r = !0 } = e, { container: u = !0 } = e, { max_lines: m } = e, { type: w = "text" } = e, { show_copy_button: q = !1 } = e, { rtl: M = !1 } = e, { autofocus: S = !1 } = e, { text_align: z = void 0 } = e, { autoscroll: F = !0 } = e, d, y = !1, N;
  const h = Vn();
  Ln(() => {
    d && d.offsetHeight + d.scrollTop > d.scrollHeight - 100;
  });
  function K() {
    h("change", n), i || h("input");
  }
  Tn(() => {
    S && d.focus(), t(21, i = !1);
  });
  async function X() {
    "clipboard" in navigator && (await navigator.clipboard.writeText(n), W());
  }
  function W() {
    t(15, y = !0), N && clearTimeout(N), N = setTimeout(
      () => {
        t(15, y = !1);
      },
      1e3
    );
  }
  function D(c) {
    const Z = c.target, Pe = Z.value, re = [Z.selectionStart, Z.selectionEnd];
    h("select", { value: Pe.substring(...re), index: re });
  }
  async function ie(c) {
    await at(), (c.key === "Enter" && c.shiftKey && s > 1 || c.key === "Enter" && !c.shiftKey && s === 1 && m >= 1) && (c.preventDefault(), h("submit"));
  }
  function ae(c) {
    const Z = c.target;
    Z.scrollTop, Z.scrollHeight - Z.clientHeight;
  }
  async function E(c) {
    if (await at(), s === m)
      return;
    let Z = m === void 0 ? !1 : m === void 0 ? 21 * 11 : 21 * (m + 1), Pe = 21 * (s + 1);
    const re = c.target;
    Z && re.scrollHeight > Z || re.scrollHeight < Pe || re.scrollHeight;
  }
  function J(c, Z) {
    if (s !== m && (c.style.overflowY = "scroll", c.addEventListener("input", E), !!Z.trim()))
      return E({ target: c }), {
        destroy: () => c.removeEventListener("input", E)
      };
  }
  function H(c) {
    te.call(this, l, c);
  }
  function _e(c) {
    te.call(this, l, c);
  }
  function ke(c) {
    te.call(this, l, c);
  }
  function b(c) {
    te.call(this, l, c);
  }
  function qe(c) {
    te.call(this, l, c);
  }
  function Ce(c) {
    te.call(this, l, c);
  }
  function He(c) {
    te.call(this, l, c);
  }
  function Ze(c) {
    te.call(this, l, c);
  }
  function g() {
    n = this.value, t(0, n);
  }
  function Yt(c) {
    Se[c ? "unshift" : "push"](() => {
      d = c, t(14, d);
    });
  }
  function Kt() {
    n = this.value, t(0, n);
  }
  function Xt(c) {
    Se[c ? "unshift" : "push"](() => {
      d = c, t(14, d);
    });
  }
  function Gt() {
    n = this.value, t(0, n);
  }
  function Ot(c) {
    Se[c ? "unshift" : "push"](() => {
      d = c, t(14, d);
    });
  }
  function Rt() {
    n = this.value, t(0, n);
  }
  function Wt(c) {
    Se[c ? "unshift" : "push"](() => {
      d = c, t(14, d);
    });
  }
  return l.$$set = (c) => {
    "value" in c && t(0, n = c.value), "value_is_output" in c && t(21, i = c.value_is_output), "lines" in c && t(1, s = c.lines), "placeholder" in c && t(2, o = c.placeholder), "label" in c && t(3, f = c.label), "info" in c && t(4, a = c.info), "disabled" in c && t(5, _ = c.disabled), "show_label" in c && t(6, r = c.show_label), "container" in c && t(7, u = c.container), "max_lines" in c && t(8, m = c.max_lines), "type" in c && t(9, w = c.type), "show_copy_button" in c && t(10, q = c.show_copy_button), "rtl" in c && t(11, M = c.rtl), "autofocus" in c && t(12, S = c.autofocus), "text_align" in c && t(13, z = c.text_align), "autoscroll" in c && t(22, F = c.autoscroll);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    1 && n === null && t(0, n = ""), l.$$.dirty[0] & /*value, el, lines, max_lines*/
    16643 && d && s !== m && E({ target: d }), l.$$.dirty[0] & /*value*/
    1 && K();
  }, [
    n,
    s,
    o,
    f,
    a,
    _,
    r,
    u,
    m,
    w,
    q,
    M,
    S,
    z,
    d,
    y,
    X,
    D,
    ie,
    ae,
    J,
    i,
    F,
    H,
    _e,
    ke,
    b,
    qe,
    Ce,
    He,
    Ze,
    g,
    Yt,
    Kt,
    Xt,
    Gt,
    Ot,
    Rt,
    Wt
  ];
}
class An extends gn {
  constructor(e) {
    super(), yn(
      this,
      e,
      Dn,
      jn,
      Cn,
      {
        value: 0,
        value_is_output: 21,
        lines: 1,
        placeholder: 2,
        label: 3,
        info: 4,
        disabled: 5,
        show_label: 6,
        container: 7,
        max_lines: 8,
        type: 9,
        show_copy_button: 10,
        rtl: 11,
        autofocus: 12,
        text_align: 13,
        autoscroll: 22
      },
      null,
      [-1, -1]
    );
  }
}
function me(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
const {
  SvelteComponent: In,
  append: A,
  attr: C,
  component_subscribe: rt,
  detach: Un,
  element: Yn,
  init: Kn,
  insert: Xn,
  noop: ut,
  safe_not_equal: Gn,
  set_style: Fe,
  svg_element: I,
  toggle_class: ct
} = window.__gradio__svelte__internal, { onMount: On } = window.__gradio__svelte__internal;
function Rn(l) {
  let e, t, n, i, s, o, f, a, _, r, u, m;
  return {
    c() {
      e = Yn("div"), t = I("svg"), n = I("g"), i = I("path"), s = I("path"), o = I("path"), f = I("path"), a = I("g"), _ = I("path"), r = I("path"), u = I("path"), m = I("path"), C(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), C(i, "fill", "#FF7C00"), C(i, "fill-opacity", "0.4"), C(i, "class", "svelte-43sxxs"), C(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), C(s, "fill", "#FF7C00"), C(s, "class", "svelte-43sxxs"), C(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), C(o, "fill", "#FF7C00"), C(o, "fill-opacity", "0.4"), C(o, "class", "svelte-43sxxs"), C(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), C(f, "fill", "#FF7C00"), C(f, "class", "svelte-43sxxs"), Fe(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), C(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), C(_, "fill", "#FF7C00"), C(_, "fill-opacity", "0.4"), C(_, "class", "svelte-43sxxs"), C(r, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), C(r, "fill", "#FF7C00"), C(r, "class", "svelte-43sxxs"), C(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), C(u, "fill", "#FF7C00"), C(u, "fill-opacity", "0.4"), C(u, "class", "svelte-43sxxs"), C(m, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), C(m, "fill", "#FF7C00"), C(m, "class", "svelte-43sxxs"), Fe(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), C(t, "viewBox", "-1200 -1200 3000 3000"), C(t, "fill", "none"), C(t, "xmlns", "http://www.w3.org/2000/svg"), C(t, "class", "svelte-43sxxs"), C(e, "class", "svelte-43sxxs"), ct(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(w, q) {
      Xn(w, e, q), A(e, t), A(t, n), A(n, i), A(n, s), A(n, o), A(n, f), A(t, a), A(a, _), A(a, r), A(a, u), A(a, m);
    },
    p(w, [q]) {
      q & /*$top*/
      2 && Fe(n, "transform", "translate(" + /*$top*/
      w[1][0] + "px, " + /*$top*/
      w[1][1] + "px)"), q & /*$bottom*/
      4 && Fe(a, "transform", "translate(" + /*$bottom*/
      w[2][0] + "px, " + /*$bottom*/
      w[2][1] + "px)"), q & /*margin*/
      1 && ct(
        e,
        "margin",
        /*margin*/
        w[0]
      );
    },
    i: ut,
    o: ut,
    d(w) {
      w && Un(e);
    }
  };
}
function Wn(l, e, t) {
  let n, i, { margin: s = !0 } = e;
  const o = ot([0, 0]);
  rt(l, o, (m) => t(1, n = m));
  const f = ot([0, 0]);
  rt(l, f, (m) => t(2, i = m));
  let a;
  async function _() {
    await Promise.all([o.set([125, 140]), f.set([-125, -140])]), await Promise.all([o.set([-125, 140]), f.set([125, -140])]), await Promise.all([o.set([-125, 0]), f.set([125, -0])]), await Promise.all([o.set([125, 0]), f.set([-125, 0])]);
  }
  async function r() {
    await _(), a || r();
  }
  async function u() {
    await Promise.all([o.set([125, 0]), f.set([-125, 0])]), r();
  }
  return On(() => (u(), () => a = !0)), l.$$set = (m) => {
    "margin" in m && t(0, s = m.margin);
  }, [s, n, i, o, f];
}
class Jn extends In {
  constructor(e) {
    super(), Kn(this, e, Wn, Rn, Gn, { margin: 0 });
  }
}
const {
  SvelteComponent: Qn,
  append: oe,
  attr: G,
  binding_callbacks: dt,
  check_outros: At,
  create_component: xn,
  create_slot: $n,
  destroy_component: ei,
  destroy_each: It,
  detach: p,
  element: Q,
  empty: pe,
  ensure_array_like: Ee,
  get_all_dirty_from_scope: ti,
  get_slot_changes: li,
  group_outros: Ut,
  init: ni,
  insert: k,
  mount_component: ii,
  noop: Ye,
  safe_not_equal: si,
  set_data: j,
  set_style: le,
  space: O,
  text: T,
  toggle_class: P,
  transition_in: ge,
  transition_out: we,
  update_slot_base: oi
} = window.__gradio__svelte__internal, { tick: fi } = window.__gradio__svelte__internal, { onDestroy: ai } = window.__gradio__svelte__internal, _i = (l) => ({}), mt = (l) => ({});
function bt(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n[40] = t, n;
}
function ht(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n;
}
function ri(l) {
  let e, t = (
    /*i18n*/
    l[1]("common.error") + ""
  ), n, i, s;
  const o = (
    /*#slots*/
    l[29].error
  ), f = $n(
    o,
    l,
    /*$$scope*/
    l[28],
    mt
  );
  return {
    c() {
      e = Q("span"), n = T(t), i = O(), f && f.c(), G(e, "class", "error svelte-1txqlrd");
    },
    m(a, _) {
      k(a, e, _), oe(e, n), k(a, i, _), f && f.m(a, _), s = !0;
    },
    p(a, _) {
      (!s || _[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      a[1]("common.error") + "") && j(n, t), f && f.p && (!s || _[0] & /*$$scope*/
      268435456) && oi(
        f,
        o,
        a,
        /*$$scope*/
        a[28],
        s ? li(
          o,
          /*$$scope*/
          a[28],
          _,
          _i
        ) : ti(
          /*$$scope*/
          a[28]
        ),
        mt
      );
    },
    i(a) {
      s || (ge(f, a), s = !0);
    },
    o(a) {
      we(f, a), s = !1;
    },
    d(a) {
      a && (p(e), p(i)), f && f.d(a);
    }
  };
}
function ui(l) {
  let e, t, n, i, s, o, f, a, _, r = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && gt(l)
  );
  function u(d, y) {
    if (
      /*progress*/
      d[7]
    )
      return mi;
    if (
      /*queue_position*/
      d[2] !== null && /*queue_size*/
      d[3] !== void 0 && /*queue_position*/
      d[2] >= 0
    )
      return di;
    if (
      /*queue_position*/
      d[2] === 0
    )
      return ci;
  }
  let m = u(l), w = m && m(l), q = (
    /*timer*/
    l[5] && kt(l)
  );
  const M = [wi, gi], S = [];
  function z(d, y) {
    return (
      /*last_progress_level*/
      d[15] != null ? 0 : (
        /*show_progress*/
        d[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = z(l)) && (o = S[s] = M[s](l));
  let F = !/*timer*/
  l[5] && Lt(l);
  return {
    c() {
      r && r.c(), e = O(), t = Q("div"), w && w.c(), n = O(), q && q.c(), i = O(), o && o.c(), f = O(), F && F.c(), a = pe(), G(t, "class", "progress-text svelte-1txqlrd"), P(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), P(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(d, y) {
      r && r.m(d, y), k(d, e, y), k(d, t, y), w && w.m(t, null), oe(t, n), q && q.m(t, null), k(d, i, y), ~s && S[s].m(d, y), k(d, f, y), F && F.m(d, y), k(d, a, y), _ = !0;
    },
    p(d, y) {
      /*variant*/
      d[8] === "default" && /*show_eta_bar*/
      d[18] && /*show_progress*/
      d[6] === "full" ? r ? r.p(d, y) : (r = gt(d), r.c(), r.m(e.parentNode, e)) : r && (r.d(1), r = null), m === (m = u(d)) && w ? w.p(d, y) : (w && w.d(1), w = m && m(d), w && (w.c(), w.m(t, n))), /*timer*/
      d[5] ? q ? q.p(d, y) : (q = kt(d), q.c(), q.m(t, null)) : q && (q.d(1), q = null), (!_ || y[0] & /*variant*/
      256) && P(
        t,
        "meta-text-center",
        /*variant*/
        d[8] === "center"
      ), (!_ || y[0] & /*variant*/
      256) && P(
        t,
        "meta-text",
        /*variant*/
        d[8] === "default"
      );
      let N = s;
      s = z(d), s === N ? ~s && S[s].p(d, y) : (o && (Ut(), we(S[N], 1, 1, () => {
        S[N] = null;
      }), At()), ~s ? (o = S[s], o ? o.p(d, y) : (o = S[s] = M[s](d), o.c()), ge(o, 1), o.m(f.parentNode, f)) : o = null), /*timer*/
      d[5] ? F && (F.d(1), F = null) : F ? F.p(d, y) : (F = Lt(d), F.c(), F.m(a.parentNode, a));
    },
    i(d) {
      _ || (ge(o), _ = !0);
    },
    o(d) {
      we(o), _ = !1;
    },
    d(d) {
      d && (p(e), p(t), p(i), p(f), p(a)), r && r.d(d), w && w.d(), q && q.d(), ~s && S[s].d(d), F && F.d(d);
    }
  };
}
function gt(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = Q("div"), G(e, "class", "eta-bar svelte-1txqlrd"), le(e, "transform", t);
    },
    m(n, i) {
      k(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && le(e, "transform", t);
    },
    d(n) {
      n && p(e);
    }
  };
}
function ci(l) {
  let e;
  return {
    c() {
      e = T("processing |");
    },
    m(t, n) {
      k(t, e, n);
    },
    p: Ye,
    d(t) {
      t && p(e);
    }
  };
}
function di(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, s, o;
  return {
    c() {
      e = T("queue: "), n = T(t), i = T("/"), s = T(
        /*queue_size*/
        l[3]
      ), o = T(" |");
    },
    m(f, a) {
      k(f, e, a), k(f, n, a), k(f, i, a), k(f, s, a), k(f, o, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && j(n, t), a[0] & /*queue_size*/
      8 && j(
        s,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (p(e), p(n), p(i), p(s), p(o));
    }
  };
}
function mi(l) {
  let e, t = Ee(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = pt(ht(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = pe();
    },
    m(i, s) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, s);
      k(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = Ee(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const f = ht(i, t, o);
          n[o] ? n[o].p(f, s) : (n[o] = pt(f), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && p(e), It(n, i);
    }
  };
}
function wt(l) {
  let e, t = (
    /*p*/
    l[38].unit + ""
  ), n, i, s = " ", o;
  function f(r, u) {
    return (
      /*p*/
      r[38].length != null ? hi : bi
    );
  }
  let a = f(l), _ = a(l);
  return {
    c() {
      _.c(), e = O(), n = T(t), i = T(" | "), o = T(s);
    },
    m(r, u) {
      _.m(r, u), k(r, e, u), k(r, n, u), k(r, i, u), k(r, o, u);
    },
    p(r, u) {
      a === (a = f(r)) && _ ? _.p(r, u) : (_.d(1), _ = a(r), _ && (_.c(), _.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      r[38].unit + "") && j(n, t);
    },
    d(r) {
      r && (p(e), p(n), p(i), p(o)), _.d(r);
    }
  };
}
function bi(l) {
  let e = me(
    /*p*/
    l[38].index || 0
  ) + "", t;
  return {
    c() {
      t = T(e);
    },
    m(n, i) {
      k(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = me(
        /*p*/
        n[38].index || 0
      ) + "") && j(t, e);
    },
    d(n) {
      n && p(t);
    }
  };
}
function hi(l) {
  let e = me(
    /*p*/
    l[38].index || 0
  ) + "", t, n, i = me(
    /*p*/
    l[38].length
  ) + "", s;
  return {
    c() {
      t = T(e), n = T("/"), s = T(i);
    },
    m(o, f) {
      k(o, t, f), k(o, n, f), k(o, s, f);
    },
    p(o, f) {
      f[0] & /*progress*/
      128 && e !== (e = me(
        /*p*/
        o[38].index || 0
      ) + "") && j(t, e), f[0] & /*progress*/
      128 && i !== (i = me(
        /*p*/
        o[38].length
      ) + "") && j(s, i);
    },
    d(o) {
      o && (p(t), p(n), p(s));
    }
  };
}
function pt(l) {
  let e, t = (
    /*p*/
    l[38].index != null && wt(l)
  );
  return {
    c() {
      t && t.c(), e = pe();
    },
    m(n, i) {
      t && t.m(n, i), k(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].index != null ? t ? t.p(n, i) : (t = wt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && p(e), t && t.d(n);
    }
  };
}
function kt(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = T(
        /*formatted_timer*/
        l[20]
      ), n = T(t), i = T("s");
    },
    m(s, o) {
      k(s, e, o), k(s, n, o), k(s, i, o);
    },
    p(s, o) {
      o[0] & /*formatted_timer*/
      1048576 && j(
        e,
        /*formatted_timer*/
        s[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && j(n, t);
    },
    d(s) {
      s && (p(e), p(n), p(i));
    }
  };
}
function gi(l) {
  let e, t;
  return e = new Jn({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      xn(e.$$.fragment);
    },
    m(n, i) {
      ii(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      n[8] === "default"), e.$set(s);
    },
    i(n) {
      t || (ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      we(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ei(e, n);
    }
  };
}
function wi(l) {
  let e, t, n, i, s, o = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && vt(l)
  );
  return {
    c() {
      e = Q("div"), t = Q("div"), f && f.c(), n = O(), i = Q("div"), s = Q("div"), G(t, "class", "progress-level-inner svelte-1txqlrd"), G(s, "class", "progress-bar svelte-1txqlrd"), le(s, "width", o), G(i, "class", "progress-bar-wrap svelte-1txqlrd"), G(e, "class", "progress-level svelte-1txqlrd");
    },
    m(a, _) {
      k(a, e, _), oe(e, t), f && f.m(t, null), oe(e, n), oe(e, i), oe(i, s), l[30](s);
    },
    p(a, _) {
      /*progress*/
      a[7] != null ? f ? f.p(a, _) : (f = vt(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), _[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      a[15] * 100}%`) && le(s, "width", o);
    },
    i: Ye,
    o: Ye,
    d(a) {
      a && p(e), f && f.d(), l[30](null);
    }
  };
}
function vt(l) {
  let e, t = Ee(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Ft(bt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = pe();
    },
    m(i, s) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, s);
      k(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = Ee(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const f = bt(i, t, o);
          n[o] ? n[o].p(f, s) : (n[o] = Ft(f), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && p(e), It(n, i);
    }
  };
}
function yt(l) {
  let e, t, n, i, s = (
    /*i*/
    l[40] !== 0 && pi()
  ), o = (
    /*p*/
    l[38].desc != null && qt(l)
  ), f = (
    /*p*/
    l[38].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null && Ct()
  ), a = (
    /*progress_level*/
    l[14] != null && St(l)
  );
  return {
    c() {
      s && s.c(), e = O(), o && o.c(), t = O(), f && f.c(), n = O(), a && a.c(), i = pe();
    },
    m(_, r) {
      s && s.m(_, r), k(_, e, r), o && o.m(_, r), k(_, t, r), f && f.m(_, r), k(_, n, r), a && a.m(_, r), k(_, i, r);
    },
    p(_, r) {
      /*p*/
      _[38].desc != null ? o ? o.p(_, r) : (o = qt(_), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      _[38].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[40]
      ] != null ? f || (f = Ct(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      _[14] != null ? a ? a.p(_, r) : (a = St(_), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(_) {
      _ && (p(e), p(t), p(n), p(i)), s && s.d(_), o && o.d(_), f && f.d(_), a && a.d(_);
    }
  };
}
function pi(l) {
  let e;
  return {
    c() {
      e = T(" /");
    },
    m(t, n) {
      k(t, e, n);
    },
    d(t) {
      t && p(e);
    }
  };
}
function qt(l) {
  let e = (
    /*p*/
    l[38].desc + ""
  ), t;
  return {
    c() {
      t = T(e);
    },
    m(n, i) {
      k(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[38].desc + "") && j(t, e);
    },
    d(n) {
      n && p(t);
    }
  };
}
function Ct(l) {
  let e;
  return {
    c() {
      e = T("-");
    },
    m(t, n) {
      k(t, e, n);
    },
    d(t) {
      t && p(e);
    }
  };
}
function St(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[40]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = T(e), n = T("%");
    },
    m(i, s) {
      k(i, t, s), k(i, n, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && j(t, e);
    },
    d(i) {
      i && (p(t), p(n));
    }
  };
}
function Ft(l) {
  let e, t = (
    /*p*/
    (l[38].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null) && yt(l)
  );
  return {
    c() {
      t && t.c(), e = pe();
    },
    m(n, i) {
      t && t.m(n, i), k(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[40]
      ] != null ? t ? t.p(n, i) : (t = yt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && p(e), t && t.d(n);
    }
  };
}
function Lt(l) {
  let e, t;
  return {
    c() {
      e = Q("p"), t = T(
        /*loading_text*/
        l[9]
      ), G(e, "class", "loading svelte-1txqlrd");
    },
    m(n, i) {
      k(n, e, i), oe(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && j(
        t,
        /*loading_text*/
        n[9]
      );
    },
    d(n) {
      n && p(e);
    }
  };
}
function ki(l) {
  let e, t, n, i, s;
  const o = [ui, ri], f = [];
  function a(_, r) {
    return (
      /*status*/
      _[4] === "pending" ? 0 : (
        /*status*/
        _[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(l)) && (n = f[t] = o[t](l)), {
    c() {
      e = Q("div"), n && n.c(), G(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1txqlrd"), P(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), P(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), P(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), P(
        e,
        "border",
        /*border*/
        l[12]
      ), le(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), le(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(_, r) {
      k(_, e, r), ~t && f[t].m(e, null), l[31](e), s = !0;
    },
    p(_, r) {
      let u = t;
      t = a(_), t === u ? ~t && f[t].p(_, r) : (n && (Ut(), we(f[u], 1, 1, () => {
        f[u] = null;
      }), At()), ~t ? (n = f[t], n ? n.p(_, r) : (n = f[t] = o[t](_), n.c()), ge(n, 1), n.m(e, null)) : n = null), (!s || r[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-1txqlrd")) && G(e, "class", i), (!s || r[0] & /*variant, show_progress, status, show_progress*/
      336) && P(e, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!s || r[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && P(
        e,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!s || r[0] & /*variant, show_progress, status*/
      336) && P(
        e,
        "generating",
        /*status*/
        _[4] === "generating"
      ), (!s || r[0] & /*variant, show_progress, border*/
      4416) && P(
        e,
        "border",
        /*border*/
        _[12]
      ), r[0] & /*absolute*/
      1024 && le(
        e,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), r[0] & /*absolute*/
      1024 && le(
        e,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      s || (ge(n), s = !0);
    },
    o(_) {
      we(n), s = !1;
    },
    d(_) {
      _ && p(e), ~t && f[t].d(), l[31](null);
    }
  };
}
let Le = [], Ie = !1;
async function vi(l, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (Le.push(l), !Ie)
      Ie = !0;
    else
      return;
    await fi(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let n = 0; n < Le.length; n++) {
        const s = Le[n].getBoundingClientRect();
        (n === 0 || s.top + window.scrollY <= t[0]) && (t[0] = s.top + window.scrollY, t[1] = n);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Ie = !1, Le = [];
    });
  }
}
function yi(l, e, t) {
  let n, { $$slots: i = {}, $$scope: s } = e, { i18n: o } = e, { eta: f = null } = e, { queue: a = !1 } = e, { queue_position: _ } = e, { queue_size: r } = e, { status: u } = e, { scroll_to_output: m = !1 } = e, { timer: w = !0 } = e, { show_progress: q = "full" } = e, { message: M = null } = e, { progress: S = null } = e, { variant: z = "default" } = e, { loading_text: F = "Loading..." } = e, { absolute: d = !0 } = e, { translucent: y = !1 } = e, { border: N = !1 } = e, { autoscroll: h } = e, K, X = !1, W = 0, D = 0, ie = null, ae = 0, E = null, J, H = null, _e = !0;
  const ke = () => {
    t(25, W = performance.now()), t(26, D = 0), X = !0, b();
  };
  function b() {
    requestAnimationFrame(() => {
      t(26, D = (performance.now() - W) / 1e3), X && b();
    });
  }
  function qe() {
    t(26, D = 0), X && (X = !1);
  }
  ai(() => {
    X && qe();
  });
  let Ce = null;
  function He(g) {
    dt[g ? "unshift" : "push"](() => {
      H = g, t(16, H), t(7, S), t(14, E), t(15, J);
    });
  }
  function Ze(g) {
    dt[g ? "unshift" : "push"](() => {
      K = g, t(13, K);
    });
  }
  return l.$$set = (g) => {
    "i18n" in g && t(1, o = g.i18n), "eta" in g && t(0, f = g.eta), "queue" in g && t(21, a = g.queue), "queue_position" in g && t(2, _ = g.queue_position), "queue_size" in g && t(3, r = g.queue_size), "status" in g && t(4, u = g.status), "scroll_to_output" in g && t(22, m = g.scroll_to_output), "timer" in g && t(5, w = g.timer), "show_progress" in g && t(6, q = g.show_progress), "message" in g && t(23, M = g.message), "progress" in g && t(7, S = g.progress), "variant" in g && t(8, z = g.variant), "loading_text" in g && t(9, F = g.loading_text), "absolute" in g && t(10, d = g.absolute), "translucent" in g && t(11, y = g.translucent), "border" in g && t(12, N = g.border), "autoscroll" in g && t(24, h = g.autoscroll), "$$scope" in g && t(28, s = g.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (f === null ? t(0, f = ie) : a && t(0, f = (performance.now() - W) / 1e3 + f), f != null && (t(19, Ce = f.toFixed(1)), t(27, ie = f))), l.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && t(17, ae = f === null || f <= 0 || !D ? null : Math.min(D / f, 1)), l.$$.dirty[0] & /*progress*/
    128 && S != null && t(18, _e = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (S != null ? t(14, E = S.map((g) => {
      if (g.index != null && g.length != null)
        return g.index / g.length;
      if (g.progress != null)
        return g.progress;
    })) : t(14, E = null), E ? (t(15, J = E[E.length - 1]), H && (J === 0 ? t(16, H.style.transition = "0", H) : t(16, H.style.transition = "150ms", H))) : t(15, J = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? ke() : qe()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && K && m && (u === "pending" || u === "complete") && vi(K, h), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = D.toFixed(1));
  }, [
    f,
    o,
    _,
    r,
    u,
    w,
    q,
    S,
    z,
    F,
    d,
    y,
    N,
    K,
    E,
    J,
    H,
    ae,
    _e,
    Ce,
    n,
    a,
    m,
    M,
    h,
    W,
    D,
    ie,
    s,
    i,
    He,
    Ze
  ];
}
class qi extends Qn {
  constructor(e) {
    super(), ni(
      this,
      e,
      yi,
      ki,
      si,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Ci,
  add_iframe_resize_listener: Si,
  add_render_callback: Fi,
  append: Li,
  attr: Ti,
  binding_callbacks: Vi,
  detach: zi,
  element: Mi,
  init: Ni,
  insert: Ei,
  noop: Tt,
  safe_not_equal: Bi,
  set_data: Hi,
  text: Zi,
  toggle_class: de
} = window.__gradio__svelte__internal, { onMount: Pi } = window.__gradio__svelte__internal;
function ji(l) {
  let e, t, n;
  return {
    c() {
      e = Mi("div"), t = Zi(
        /*value*/
        l[0]
      ), Ti(e, "class", "svelte-84cxb8"), Fi(() => (
        /*div_elementresize_handler*/
        l[5].call(e)
      )), de(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), de(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), de(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    m(i, s) {
      Ei(i, e, s), Li(e, t), n = Si(
        e,
        /*div_elementresize_handler*/
        l[5].bind(e)
      ), l[6](e);
    },
    p(i, [s]) {
      s & /*value*/
      1 && Hi(
        t,
        /*value*/
        i[0]
      ), s & /*type*/
      2 && de(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), s & /*type*/
      2 && de(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), s & /*selected*/
      4 && de(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    i: Tt,
    o: Tt,
    d(i) {
      i && zi(e), n(), l[6](null);
    }
  };
}
function Di(l, e, t) {
  let { value: n } = e, { type: i } = e, { selected: s = !1 } = e, o, f;
  function a(u, m) {
    !u || !m || (f.style.setProperty("--local-text-width", `${m < 150 ? m : 200}px`), t(4, f.style.whiteSpace = "unset", f));
  }
  Pi(() => {
    a(f, o);
  });
  function _() {
    o = this.clientWidth, t(3, o);
  }
  function r(u) {
    Vi[u ? "unshift" : "push"](() => {
      f = u, t(4, f);
    });
  }
  return l.$$set = (u) => {
    "value" in u && t(0, n = u.value), "type" in u && t(1, i = u.type), "selected" in u && t(2, s = u.selected);
  }, [n, i, s, o, f, _, r];
}
class es extends Ci {
  constructor(e) {
    super(), Ni(this, e, Di, ji, Bi, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: Ai,
  add_flush_callback: Vt,
  assign: Ii,
  bind: zt,
  binding_callbacks: Mt,
  check_outros: Ui,
  create_component: We,
  destroy_component: Je,
  detach: Yi,
  flush: L,
  get_spread_object: Ki,
  get_spread_update: Xi,
  group_outros: Gi,
  init: Oi,
  insert: Ri,
  mount_component: Qe,
  safe_not_equal: Wi,
  space: Ji,
  transition_in: be,
  transition_out: ye
} = window.__gradio__svelte__internal;
function Nt(l) {
  let e, t;
  const n = [
    { autoscroll: (
      /*gradio*/
      l[2].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[2].i18n
    ) },
    /*loading_status*/
    l[17]
  ];
  let i = {};
  for (let s = 0; s < n.length; s += 1)
    i = Ii(i, n[s]);
  return e = new qi({ props: i }), {
    c() {
      We(e.$$.fragment);
    },
    m(s, o) {
      Qe(e, s, o), t = !0;
    },
    p(s, o) {
      const f = o[0] & /*gradio, loading_status*/
      131076 ? Xi(n, [
        o[0] & /*gradio*/
        4 && { autoscroll: (
          /*gradio*/
          s[2].autoscroll
        ) },
        o[0] & /*gradio*/
        4 && { i18n: (
          /*gradio*/
          s[2].i18n
        ) },
        o[0] & /*loading_status*/
        131072 && Ki(
          /*loading_status*/
          s[17]
        )
      ]) : {};
      e.$set(f);
    },
    i(s) {
      t || (be(e.$$.fragment, s), t = !0);
    },
    o(s) {
      ye(e.$$.fragment, s), t = !1;
    },
    d(s) {
      Je(e, s);
    }
  };
}
function Qi(l) {
  let e, t, n, i, s, o = (
    /*loading_status*/
    l[17] && Nt(l)
  );
  function f(r) {
    l[23](r);
  }
  function a(r) {
    l[24](r);
  }
  let _ = {
    label: (
      /*label*/
      l[3]
    ),
    info: (
      /*info*/
      l[4]
    ),
    show_label: (
      /*show_label*/
      l[10]
    ),
    lines: (
      /*lines*/
      l[8]
    ),
    type: (
      /*type*/
      l[12]
    ),
    rtl: (
      /*rtl*/
      l[18]
    ),
    text_align: (
      /*text_align*/
      l[19]
    ),
    max_lines: /*max_lines*/ l[11] ? (
      /*max_lines*/
      l[11]
    ) : (
      /*lines*/
      l[8] + 1
    ),
    placeholder: (
      /*placeholder*/
      l[9]
    ),
    show_copy_button: (
      /*show_copy_button*/
      l[16]
    ),
    autofocus: (
      /*autofocus*/
      l[20]
    ),
    container: (
      /*container*/
      l[13]
    ),
    autoscroll: (
      /*autoscroll*/
      l[21]
    ),
    disabled: !/*interactive*/
    l[22]
  };
  return (
    /*value*/
    l[0] !== void 0 && (_.value = /*value*/
    l[0]), /*value_is_output*/
    l[1] !== void 0 && (_.value_is_output = /*value_is_output*/
    l[1]), t = new An({ props: _ }), Mt.push(() => zt(t, "value", f)), Mt.push(() => zt(t, "value_is_output", a)), t.$on(
      "change",
      /*change_handler*/
      l[25]
    ), t.$on(
      "input",
      /*input_handler*/
      l[26]
    ), t.$on(
      "submit",
      /*submit_handler*/
      l[27]
    ), t.$on(
      "blur",
      /*blur_handler*/
      l[28]
    ), t.$on(
      "select",
      /*select_handler*/
      l[29]
    ), t.$on(
      "focus",
      /*focus_handler*/
      l[30]
    ), {
      c() {
        o && o.c(), e = Ji(), We(t.$$.fragment);
      },
      m(r, u) {
        o && o.m(r, u), Ri(r, e, u), Qe(t, r, u), s = !0;
      },
      p(r, u) {
        /*loading_status*/
        r[17] ? o ? (o.p(r, u), u[0] & /*loading_status*/
        131072 && be(o, 1)) : (o = Nt(r), o.c(), be(o, 1), o.m(e.parentNode, e)) : o && (Gi(), ye(o, 1, 1, () => {
          o = null;
        }), Ui());
        const m = {};
        u[0] & /*label*/
        8 && (m.label = /*label*/
        r[3]), u[0] & /*info*/
        16 && (m.info = /*info*/
        r[4]), u[0] & /*show_label*/
        1024 && (m.show_label = /*show_label*/
        r[10]), u[0] & /*lines*/
        256 && (m.lines = /*lines*/
        r[8]), u[0] & /*type*/
        4096 && (m.type = /*type*/
        r[12]), u[0] & /*rtl*/
        262144 && (m.rtl = /*rtl*/
        r[18]), u[0] & /*text_align*/
        524288 && (m.text_align = /*text_align*/
        r[19]), u[0] & /*max_lines, lines*/
        2304 && (m.max_lines = /*max_lines*/
        r[11] ? (
          /*max_lines*/
          r[11]
        ) : (
          /*lines*/
          r[8] + 1
        )), u[0] & /*placeholder*/
        512 && (m.placeholder = /*placeholder*/
        r[9]), u[0] & /*show_copy_button*/
        65536 && (m.show_copy_button = /*show_copy_button*/
        r[16]), u[0] & /*autofocus*/
        1048576 && (m.autofocus = /*autofocus*/
        r[20]), u[0] & /*container*/
        8192 && (m.container = /*container*/
        r[13]), u[0] & /*autoscroll*/
        2097152 && (m.autoscroll = /*autoscroll*/
        r[21]), u[0] & /*interactive*/
        4194304 && (m.disabled = !/*interactive*/
        r[22]), !n && u[0] & /*value*/
        1 && (n = !0, m.value = /*value*/
        r[0], Vt(() => n = !1)), !i && u[0] & /*value_is_output*/
        2 && (i = !0, m.value_is_output = /*value_is_output*/
        r[1], Vt(() => i = !1)), t.$set(m);
      },
      i(r) {
        s || (be(o), be(t.$$.fragment, r), s = !0);
      },
      o(r) {
        ye(o), ye(t.$$.fragment, r), s = !1;
      },
      d(r) {
        r && Yi(e), o && o.d(r), Je(t, r);
      }
    }
  );
}
function xi(l) {
  let e, t;
  return e = new ul({
    props: {
      visible: (
        /*visible*/
        l[7]
      ),
      elem_id: (
        /*elem_id*/
        l[5]
      ),
      elem_classes: (
        /*elem_classes*/
        l[6]
      ),
      scale: (
        /*scale*/
        l[14]
      ),
      min_width: (
        /*min_width*/
        l[15]
      ),
      allow_overflow: !1,
      padding: (
        /*container*/
        l[13]
      ),
      $$slots: { default: [Qi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      We(e.$$.fragment);
    },
    m(n, i) {
      Qe(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*visible*/
      128 && (s.visible = /*visible*/
      n[7]), i[0] & /*elem_id*/
      32 && (s.elem_id = /*elem_id*/
      n[5]), i[0] & /*elem_classes*/
      64 && (s.elem_classes = /*elem_classes*/
      n[6]), i[0] & /*scale*/
      16384 && (s.scale = /*scale*/
      n[14]), i[0] & /*min_width*/
      32768 && (s.min_width = /*min_width*/
      n[15]), i[0] & /*container*/
      8192 && (s.padding = /*container*/
      n[13]), i[0] & /*label, info, show_label, lines, type, rtl, text_align, max_lines, placeholder, show_copy_button, autofocus, container, autoscroll, interactive, value, value_is_output, gradio, loading_status*/
      8339231 | i[1] & /*$$scope*/
      1 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (be(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ye(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Je(e, n);
    }
  };
}
function $i(l, e, t) {
  let { gradio: n } = e, { label: i = "Textbox" } = e, { info: s = void 0 } = e, { elem_id: o = "" } = e, { elem_classes: f = [] } = e, { visible: a = !0 } = e, { value: _ = "" } = e, { lines: r } = e, { placeholder: u = "" } = e, { show_label: m } = e, { max_lines: w } = e, { type: q = "text" } = e, { container: M = !0 } = e, { scale: S = null } = e, { min_width: z = void 0 } = e, { show_copy_button: F = !1 } = e, { loading_status: d = void 0 } = e, { value_is_output: y = !1 } = e, { rtl: N = !1 } = e, { text_align: h = void 0 } = e, { autofocus: K = !1 } = e, { autoscroll: X = !0 } = e, { interactive: W } = e;
  function D(b) {
    _ = b, t(0, _);
  }
  function ie(b) {
    y = b, t(1, y);
  }
  const ae = () => n.dispatch("change", _), E = () => n.dispatch("input"), J = () => n.dispatch("submit"), H = () => n.dispatch("blur"), _e = (b) => n.dispatch("select", b.detail), ke = () => n.dispatch("focus");
  return l.$$set = (b) => {
    "gradio" in b && t(2, n = b.gradio), "label" in b && t(3, i = b.label), "info" in b && t(4, s = b.info), "elem_id" in b && t(5, o = b.elem_id), "elem_classes" in b && t(6, f = b.elem_classes), "visible" in b && t(7, a = b.visible), "value" in b && t(0, _ = b.value), "lines" in b && t(8, r = b.lines), "placeholder" in b && t(9, u = b.placeholder), "show_label" in b && t(10, m = b.show_label), "max_lines" in b && t(11, w = b.max_lines), "type" in b && t(12, q = b.type), "container" in b && t(13, M = b.container), "scale" in b && t(14, S = b.scale), "min_width" in b && t(15, z = b.min_width), "show_copy_button" in b && t(16, F = b.show_copy_button), "loading_status" in b && t(17, d = b.loading_status), "value_is_output" in b && t(1, y = b.value_is_output), "rtl" in b && t(18, N = b.rtl), "text_align" in b && t(19, h = b.text_align), "autofocus" in b && t(20, K = b.autofocus), "autoscroll" in b && t(21, X = b.autoscroll), "interactive" in b && t(22, W = b.interactive);
  }, [
    _,
    y,
    n,
    i,
    s,
    o,
    f,
    a,
    r,
    u,
    m,
    w,
    q,
    M,
    S,
    z,
    F,
    d,
    N,
    h,
    K,
    X,
    W,
    D,
    ie,
    ae,
    E,
    J,
    H,
    _e,
    ke
  ];
}
class ts extends Ai {
  constructor(e) {
    super(), Oi(
      this,
      e,
      $i,
      xi,
      Wi,
      {
        gradio: 2,
        label: 3,
        info: 4,
        elem_id: 5,
        elem_classes: 6,
        visible: 7,
        value: 0,
        lines: 8,
        placeholder: 9,
        show_label: 10,
        max_lines: 11,
        type: 12,
        container: 13,
        scale: 14,
        min_width: 15,
        show_copy_button: 16,
        loading_status: 17,
        value_is_output: 1,
        rtl: 18,
        text_align: 19,
        autofocus: 20,
        autoscroll: 21,
        interactive: 22
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[2];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), L();
  }
  get label() {
    return this.$$.ctx[3];
  }
  set label(e) {
    this.$$set({ label: e }), L();
  }
  get info() {
    return this.$$.ctx[4];
  }
  set info(e) {
    this.$$set({ info: e }), L();
  }
  get elem_id() {
    return this.$$.ctx[5];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), L();
  }
  get elem_classes() {
    return this.$$.ctx[6];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), L();
  }
  get visible() {
    return this.$$.ctx[7];
  }
  set visible(e) {
    this.$$set({ visible: e }), L();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), L();
  }
  get lines() {
    return this.$$.ctx[8];
  }
  set lines(e) {
    this.$$set({ lines: e }), L();
  }
  get placeholder() {
    return this.$$.ctx[9];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), L();
  }
  get show_label() {
    return this.$$.ctx[10];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), L();
  }
  get max_lines() {
    return this.$$.ctx[11];
  }
  set max_lines(e) {
    this.$$set({ max_lines: e }), L();
  }
  get type() {
    return this.$$.ctx[12];
  }
  set type(e) {
    this.$$set({ type: e }), L();
  }
  get container() {
    return this.$$.ctx[13];
  }
  set container(e) {
    this.$$set({ container: e }), L();
  }
  get scale() {
    return this.$$.ctx[14];
  }
  set scale(e) {
    this.$$set({ scale: e }), L();
  }
  get min_width() {
    return this.$$.ctx[15];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), L();
  }
  get show_copy_button() {
    return this.$$.ctx[16];
  }
  set show_copy_button(e) {
    this.$$set({ show_copy_button: e }), L();
  }
  get loading_status() {
    return this.$$.ctx[17];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), L();
  }
  get value_is_output() {
    return this.$$.ctx[1];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), L();
  }
  get rtl() {
    return this.$$.ctx[18];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), L();
  }
  get text_align() {
    return this.$$.ctx[19];
  }
  set text_align(e) {
    this.$$set({ text_align: e }), L();
  }
  get autofocus() {
    return this.$$.ctx[20];
  }
  set autofocus(e) {
    this.$$set({ autofocus: e }), L();
  }
  get autoscroll() {
    return this.$$.ctx[21];
  }
  set autoscroll(e) {
    this.$$set({ autoscroll: e }), L();
  }
  get interactive() {
    return this.$$.ctx[22];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), L();
  }
}
export {
  es as BaseExample,
  An as BaseTextbox,
  ts as default
};
