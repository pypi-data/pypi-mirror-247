const {
  SvelteComponent: tl,
  assign: ll,
  create_slot: nl,
  detach: il,
  element: sl,
  get_all_dirty_from_scope: ol,
  get_slot_changes: fl,
  get_spread_update: al,
  init: _l,
  insert: rl,
  safe_not_equal: ul,
  set_dynamic_element_data: $e,
  set_style: H,
  toggle_class: le,
  transition_in: Bt,
  transition_out: Ht,
  update_slot_base: cl
} = window.__gradio__svelte__internal;
function dl(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), s = nl(
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
    f = ll(f, o[a]);
  return {
    c() {
      e = sl(
        /*tag*/
        l[14]
      ), s && s.c(), $e(
        /*tag*/
        l[14]
      )(e, f), le(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), le(
        e,
        "padded",
        /*padding*/
        l[6]
      ), le(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), le(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), H(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), H(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), H(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), H(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), H(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), H(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), H(e, "border-width", "var(--block-border-width)");
    },
    m(a, _) {
      rl(a, e, _), s && s.m(e, null), n = !0;
    },
    p(a, _) {
      s && s.p && (!n || _ & /*$$scope*/
      131072) && cl(
        s,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? fl(
          i,
          /*$$scope*/
          a[17],
          _,
          null
        ) : ol(
          /*$$scope*/
          a[17]
        ),
        null
      ), $e(
        /*tag*/
        a[14]
      )(e, f = al(o, [
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
      ])), le(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), le(
        e,
        "padded",
        /*padding*/
        a[6]
      ), le(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), le(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), _ & /*height*/
      1 && H(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), _ & /*width*/
      2 && H(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), _ & /*variant*/
      16 && H(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), _ & /*allow_overflow*/
      2048 && H(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && H(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), _ & /*min_width*/
      8192 && H(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (Bt(s, a), n = !0);
    },
    o(a) {
      Ht(s, a), n = !1;
    },
    d(a) {
      a && il(e), s && s.d(a);
    }
  };
}
function ml(l) {
  let e, t = (
    /*tag*/
    l[14] && dl(l)
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
      e || (Bt(t, n), e = !0);
    },
    o(n) {
      Ht(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function bl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: o = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: _ = "solid" } = e, { border_mode: r = "base" } = e, { padding: u = !0 } = e, { type: m = "normal" } = e, { test_id: w = void 0 } = e, { explicit_call: q = !1 } = e, { container: M = !0 } = e, { visible: S = !0 } = e, { allow_overflow: z = !0 } = e, { scale: F = null } = e, { min_width: c = 0 } = e, y = m === "fieldset" ? "fieldset" : "div";
  const N = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return l.$$set = (g) => {
    "height" in g && t(0, s = g.height), "width" in g && t(1, o = g.width), "elem_id" in g && t(2, f = g.elem_id), "elem_classes" in g && t(3, a = g.elem_classes), "variant" in g && t(4, _ = g.variant), "border_mode" in g && t(5, r = g.border_mode), "padding" in g && t(6, u = g.padding), "type" in g && t(16, m = g.type), "test_id" in g && t(7, w = g.test_id), "explicit_call" in g && t(8, q = g.explicit_call), "container" in g && t(9, M = g.container), "visible" in g && t(10, S = g.visible), "allow_overflow" in g && t(11, z = g.allow_overflow), "scale" in g && t(12, F = g.scale), "min_width" in g && t(13, c = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
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
    c,
    y,
    N,
    m,
    i,
    n
  ];
}
class hl extends tl {
  constructor(e) {
    super(), _l(this, e, bl, ml, ul, {
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
  SvelteComponent: gl,
  attr: wl,
  create_slot: pl,
  detach: kl,
  element: vl,
  get_all_dirty_from_scope: yl,
  get_slot_changes: ql,
  init: Cl,
  insert: Sl,
  safe_not_equal: Fl,
  transition_in: Ll,
  transition_out: Tl,
  update_slot_base: Vl
} = window.__gradio__svelte__internal;
function zl(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = pl(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = vl("div"), i && i.c(), wl(e, "class", "svelte-1hnfib2");
    },
    m(s, o) {
      Sl(s, e, o), i && i.m(e, null), t = !0;
    },
    p(s, [o]) {
      i && i.p && (!t || o & /*$$scope*/
      1) && Vl(
        i,
        n,
        s,
        /*$$scope*/
        s[0],
        t ? ql(
          n,
          /*$$scope*/
          s[0],
          o,
          null
        ) : yl(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (Ll(i, s), t = !0);
    },
    o(s) {
      Tl(i, s), t = !1;
    },
    d(s) {
      s && kl(e), i && i.d(s);
    }
  };
}
function Ml(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, n];
}
class Nl extends gl {
  constructor(e) {
    super(), Cl(this, e, Ml, zl, Fl, {});
  }
}
const {
  SvelteComponent: El,
  attr: et,
  check_outros: Bl,
  create_component: Hl,
  create_slot: Zl,
  destroy_component: Pl,
  detach: ze,
  element: jl,
  empty: Dl,
  get_all_dirty_from_scope: Al,
  get_slot_changes: Il,
  group_outros: Ul,
  init: Yl,
  insert: Me,
  mount_component: Kl,
  safe_not_equal: Xl,
  set_data: Gl,
  space: Ol,
  text: Rl,
  toggle_class: de,
  transition_in: qe,
  transition_out: Ne,
  update_slot_base: Wl
} = window.__gradio__svelte__internal;
function tt(l) {
  let e, t;
  return e = new Nl({
    props: {
      $$slots: { default: [Jl] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Hl(e.$$.fragment);
    },
    m(n, i) {
      Kl(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: n }), e.$set(s);
    },
    i(n) {
      t || (qe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ne(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Pl(e, n);
    }
  };
}
function Jl(l) {
  let e;
  return {
    c() {
      e = Rl(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Me(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Gl(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && ze(e);
    }
  };
}
function Ql(l) {
  let e, t, n, i;
  const s = (
    /*#slots*/
    l[2].default
  ), o = Zl(
    s,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let f = (
    /*info*/
    l[1] && tt(l)
  );
  return {
    c() {
      e = jl("span"), o && o.c(), t = Ol(), f && f.c(), n = Dl(), et(e, "data-testid", "block-info"), et(e, "class", "svelte-22c38v"), de(e, "sr-only", !/*show_label*/
      l[0]), de(e, "hide", !/*show_label*/
      l[0]), de(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(a, _) {
      Me(a, e, _), o && o.m(e, null), Me(a, t, _), f && f.m(a, _), Me(a, n, _), i = !0;
    },
    p(a, [_]) {
      o && o.p && (!i || _ & /*$$scope*/
      8) && Wl(
        o,
        s,
        a,
        /*$$scope*/
        a[3],
        i ? Il(
          s,
          /*$$scope*/
          a[3],
          _,
          null
        ) : Al(
          /*$$scope*/
          a[3]
        ),
        null
      ), (!i || _ & /*show_label*/
      1) && de(e, "sr-only", !/*show_label*/
      a[0]), (!i || _ & /*show_label*/
      1) && de(e, "hide", !/*show_label*/
      a[0]), (!i || _ & /*info*/
      2) && de(
        e,
        "has-info",
        /*info*/
        a[1] != null
      ), /*info*/
      a[1] ? f ? (f.p(a, _), _ & /*info*/
      2 && qe(f, 1)) : (f = tt(a), f.c(), qe(f, 1), f.m(n.parentNode, n)) : f && (Ul(), Ne(f, 1, 1, () => {
        f = null;
      }), Bl());
    },
    i(a) {
      i || (qe(o, a), qe(f), i = !0);
    },
    o(a) {
      Ne(o, a), Ne(f), i = !1;
    },
    d(a) {
      a && (ze(e), ze(t), ze(n)), o && o.d(a), f && f.d(a);
    }
  };
}
function xl(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: o = void 0 } = e;
  return l.$$set = (f) => {
    "show_label" in f && t(0, s = f.show_label), "info" in f && t(1, o = f.info), "$$scope" in f && t(3, i = f.$$scope);
  }, [s, o, n, i];
}
class $l extends El {
  constructor(e) {
    super(), Yl(this, e, xl, Ql, Xl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: en,
  append: tn,
  attr: ne,
  detach: ln,
  init: nn,
  insert: sn,
  noop: De,
  safe_not_equal: on,
  svg_element: lt
} = window.__gradio__svelte__internal;
function fn(l) {
  let e, t;
  return {
    c() {
      e = lt("svg"), t = lt("polyline"), ne(t, "points", "20 6 9 17 4 12"), ne(e, "xmlns", "http://www.w3.org/2000/svg"), ne(e, "viewBox", "2 0 20 20"), ne(e, "fill", "none"), ne(e, "stroke", "currentColor"), ne(e, "stroke-width", "3"), ne(e, "stroke-linecap", "round"), ne(e, "stroke-linejoin", "round");
    },
    m(n, i) {
      sn(n, e, i), tn(e, t);
    },
    p: De,
    i: De,
    o: De,
    d(n) {
      n && ln(e);
    }
  };
}
class an extends en {
  constructor(e) {
    super(), nn(this, e, null, fn, on, {});
  }
}
const {
  SvelteComponent: _n,
  append: nt,
  attr: ae,
  detach: rn,
  init: un,
  insert: cn,
  noop: Ae,
  safe_not_equal: dn,
  svg_element: Ie
} = window.__gradio__svelte__internal;
function mn(l) {
  let e, t, n;
  return {
    c() {
      e = Ie("svg"), t = Ie("path"), n = Ie("path"), ae(t, "fill", "currentColor"), ae(t, "d", "M28 10v18H10V10h18m0-2H10a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2Z"), ae(n, "fill", "currentColor"), ae(n, "d", "M4 18H2V4a2 2 0 0 1 2-2h14v2H4Z"), ae(e, "xmlns", "http://www.w3.org/2000/svg"), ae(e, "viewBox", "0 0 33 33"), ae(e, "color", "currentColor");
    },
    m(i, s) {
      cn(i, e, s), nt(e, t), nt(e, n);
    },
    p: Ae,
    i: Ae,
    o: Ae,
    d(i) {
      i && rn(e);
    }
  };
}
class bn extends _n {
  constructor(e) {
    super(), un(this, e, null, mn, dn, {});
  }
}
const hn = [
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
], it = {
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
hn.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: it[e][t],
      secondary: it[e][n]
    }
  }),
  {}
);
function Ee() {
}
const gn = (l) => l;
function wn(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Zt = typeof window < "u";
let st = Zt ? () => window.performance.now() : () => Date.now(), Pt = Zt ? (l) => requestAnimationFrame(l) : Ee;
const we = /* @__PURE__ */ new Set();
function jt(l) {
  we.forEach((e) => {
    e.c(l) || (we.delete(e), e.f());
  }), we.size !== 0 && Pt(jt);
}
function pn(l) {
  let e;
  return we.size === 0 && Pt(jt), {
    promise: new Promise((t) => {
      we.add(e = { c: l, f: t });
    }),
    abort() {
      we.delete(e);
    }
  };
}
function kn(l, { delay: e = 0, duration: t = 400, easing: n = gn } = {}) {
  const i = +getComputedStyle(l).opacity;
  return {
    delay: e,
    duration: t,
    easing: n,
    css: (s) => `opacity: ${s * i}`
  };
}
const me = [];
function vn(l, e = Ee) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (wn(l, f) && (l = f, t)) {
      const a = !me.length;
      for (const _ of n)
        _[1](), me.push(_, l);
      if (a) {
        for (let _ = 0; _ < me.length; _ += 2)
          me[_][0](me[_ + 1]);
        me.length = 0;
      }
    }
  }
  function s(f) {
    i(f(l));
  }
  function o(f, a = Ee) {
    const _ = [f, a];
    return n.add(_), n.size === 1 && (t = e(i, s) || Ee), f(l), () => {
      n.delete(_), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: o };
}
function ot(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function Ye(l, e, t, n) {
  if (typeof t == "number" || ot(t)) {
    const i = n - t, s = (t - e) / (l.dt || 1 / 60), o = l.opts.stiffness * i, f = l.opts.damping * s, a = (o - f) * l.inv_mass, _ = (s + a) * l.dt;
    return Math.abs(_) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, ot(t) ? new Date(t.getTime() + _) : t + _);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => Ye(l, e[s], t[s], n[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = Ye(l, e[s], t[s], n[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function ft(l, e = {}) {
  const t = vn(l), { stiffness: n = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let o, f, a, _ = l, r = l, u = 1, m = 0, w = !1;
  function q(S, z = {}) {
    r = S;
    const F = a = {};
    return l == null || z.hard || M.stiffness >= 1 && M.damping >= 1 ? (w = !0, o = st(), _ = S, t.set(l = r), Promise.resolve()) : (z.soft && (m = 1 / ((z.soft === !0 ? 0.5 : +z.soft) * 60), u = 0), f || (o = st(), w = !1, f = pn((c) => {
      if (w)
        return w = !1, f = null, !1;
      u = Math.min(u + m, 1);
      const y = {
        inv_mass: u,
        opts: M,
        settled: !0,
        dt: (c - o) * 60 / 1e3
      }, N = Ye(y, _, l, r);
      return o = c, _ = l, t.set(l = N), y.settled && (f = null), !y.settled;
    })), new Promise((c) => {
      f.promise.then(() => {
        F === a && c();
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
  SvelteComponent: yn,
  action_destroyer: qn,
  add_render_callback: Cn,
  append: Sn,
  attr: v,
  binding_callbacks: Le,
  bubble: ie,
  check_outros: Xe,
  create_component: Ge,
  create_in_transition: Fn,
  destroy_component: Oe,
  detach: X,
  element: re,
  empty: Dt,
  group_outros: Re,
  init: Ln,
  insert: G,
  is_function: Tn,
  listen: V,
  mount_component: We,
  noop: Be,
  run_all: Ze,
  safe_not_equal: Vn,
  set_data: zn,
  set_input_value: oe,
  space: At,
  text: Mn,
  toggle_class: at,
  transition_in: W,
  transition_out: $
} = window.__gradio__svelte__internal, { beforeUpdate: Nn, afterUpdate: En, createEventDispatcher: Bn, tick: _t } = window.__gradio__svelte__internal;
function Hn(l) {
  let e;
  return {
    c() {
      e = Mn(
        /*label*/
        l[3]
      );
    },
    m(t, n) {
      G(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      8 && zn(
        e,
        /*label*/
        t[3]
      );
    },
    d(t) {
      t && X(e);
    }
  };
}
function Zn(l) {
  let e, t, n, i, s, o, f, a, _ = (
    /*show_label*/
    l[6] && /*show_copy_button*/
    l[10] && rt(l)
  );
  return {
    c() {
      _ && _.c(), e = At(), t = re("textarea"), v(t, "data-testid", "textbox"), v(t, "class", "scroll-hide svelte-18tqgac"), v(t, "dir", n = /*rtl*/
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
      _ && _.m(r, u), G(r, e, u), G(r, t, u), oe(
        t,
        /*value*/
        l[0]
      ), l[38](t), o = !0, /*autofocus*/
      l[12] && t.focus(), f || (a = [
        qn(s = /*text_area_resize*/
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
      1088 && W(_, 1)) : (_ = rt(r), _.c(), W(_, 1), _.m(e.parentNode, e)) : _ && (Re(), $(_, 1, 1, () => {
        _ = null;
      }), Xe()), (!o || u[0] & /*rtl*/
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
      r[13] : "")) && v(t, "style", i), s && Tn(s.update) && u[0] & /*value*/
      1 && s.update.call(
        null,
        /*value*/
        r[0]
      ), u[0] & /*value*/
      1 && oe(
        t,
        /*value*/
        r[0]
      );
    },
    i(r) {
      o || (W(_), o = !0);
    },
    o(r) {
      $(_), o = !1;
    },
    d(r) {
      r && (X(e), X(t)), _ && _.d(r), l[38](null), f = !1, Ze(a);
    }
  };
}
function Pn(l) {
  let e;
  function t(s, o) {
    if (
      /*type*/
      s[9] === "text"
    )
      return Un;
    if (
      /*type*/
      s[9] === "password"
    )
      return In;
    if (
      /*type*/
      s[9] === "email"
    )
      return An;
  }
  let n = t(l), i = n && n(l);
  return {
    c() {
      i && i.c(), e = Dt();
    },
    m(s, o) {
      i && i.m(s, o), G(s, e, o);
    },
    p(s, o) {
      n === (n = t(s)) && i ? i.p(s, o) : (i && i.d(1), i = n && n(s), i && (i.c(), i.m(e.parentNode, e)));
    },
    i: Be,
    o: Be,
    d(s) {
      s && X(e), i && i.d(s);
    }
  };
}
function rt(l) {
  let e, t, n, i;
  const s = [Dn, jn], o = [];
  function f(a, _) {
    return (
      /*copied*/
      a[15] ? 0 : 1
    );
  }
  return e = f(l), t = o[e] = s[e](l), {
    c() {
      t.c(), n = Dt();
    },
    m(a, _) {
      o[e].m(a, _), G(a, n, _), i = !0;
    },
    p(a, _) {
      let r = e;
      e = f(a), e === r ? o[e].p(a, _) : (Re(), $(o[r], 1, 1, () => {
        o[r] = null;
      }), Xe(), t = o[e], t ? t.p(a, _) : (t = o[e] = s[e](a), t.c()), W(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (W(t), i = !0);
    },
    o(a) {
      $(t), i = !1;
    },
    d(a) {
      a && X(n), o[e].d(a);
    }
  };
}
function jn(l) {
  let e, t, n, i, s;
  return t = new bn({}), {
    c() {
      e = re("button"), Ge(t.$$.fragment), v(e, "aria-label", "Copy"), v(e, "aria-roledescription", "Copy text"), v(e, "class", "svelte-18tqgac");
    },
    m(o, f) {
      G(o, e, f), We(t, e, null), n = !0, i || (s = V(
        e,
        "click",
        /*handle_copy*/
        l[16]
      ), i = !0);
    },
    p: Be,
    i(o) {
      n || (W(t.$$.fragment, o), n = !0);
    },
    o(o) {
      $(t.$$.fragment, o), n = !1;
    },
    d(o) {
      o && X(e), Oe(t), i = !1, s();
    }
  };
}
function Dn(l) {
  let e, t, n, i;
  return t = new an({}), {
    c() {
      e = re("button"), Ge(t.$$.fragment), v(e, "aria-label", "Copied"), v(e, "aria-roledescription", "Text copied"), v(e, "class", "svelte-18tqgac");
    },
    m(s, o) {
      G(s, e, o), We(t, e, null), i = !0;
    },
    p: Be,
    i(s) {
      i || (W(t.$$.fragment, s), s && (n || Cn(() => {
        n = Fn(e, kn, { duration: 300 }), n.start();
      })), i = !0);
    },
    o(s) {
      $(t.$$.fragment, s), i = !1;
    },
    d(s) {
      s && X(e), Oe(t);
    }
  };
}
function An(l) {
  let e, t, n;
  return {
    c() {
      e = re("input"), v(e, "data-testid", "textbox"), v(e, "type", "email"), v(e, "class", "scroll-hide svelte-18tqgac"), v(
        e,
        "placeholder",
        /*placeholder*/
        l[2]
      ), e.disabled = /*disabled*/
      l[5], e.autofocus = /*autofocus*/
      l[12], v(e, "autocomplete", "email");
    },
    m(i, s) {
      G(i, e, s), oe(
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
      i[0] && oe(
        e,
        /*value*/
        i[0]
      );
    },
    d(i) {
      i && X(e), l[36](null), t = !1, Ze(n);
    }
  };
}
function In(l) {
  let e, t, n;
  return {
    c() {
      e = re("input"), v(e, "data-testid", "password"), v(e, "type", "password"), v(e, "class", "scroll-hide svelte-18tqgac"), v(
        e,
        "placeholder",
        /*placeholder*/
        l[2]
      ), e.disabled = /*disabled*/
      l[5], e.autofocus = /*autofocus*/
      l[12], v(e, "autocomplete", "");
    },
    m(i, s) {
      G(i, e, s), oe(
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
      i[0] && oe(
        e,
        /*value*/
        i[0]
      );
    },
    d(i) {
      i && X(e), l[34](null), t = !1, Ze(n);
    }
  };
}
function Un(l) {
  let e, t, n, i, s;
  return {
    c() {
      e = re("input"), v(e, "data-testid", "textbox"), v(e, "type", "text"), v(e, "class", "scroll-hide svelte-18tqgac"), v(e, "dir", t = /*rtl*/
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
      G(o, e, f), oe(
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
      o[0] && oe(
        e,
        /*value*/
        o[0]
      );
    },
    d(o) {
      o && X(e), l[32](null), i = !1, Ze(s);
    }
  };
}
function Yn(l) {
  let e, t, n, i, s, o;
  t = new $l({
    props: {
      show_label: (
        /*show_label*/
        l[6]
      ),
      info: (
        /*info*/
        l[4]
      ),
      $$slots: { default: [Hn] },
      $$scope: { ctx: l }
    }
  });
  const f = [Pn, Zn], a = [];
  function _(r, u) {
    return (
      /*lines*/
      r[1] === 1 && /*max_lines*/
      r[8] === 1 ? 0 : 1
    );
  }
  return i = _(l), s = a[i] = f[i](l), {
    c() {
      e = re("label"), Ge(t.$$.fragment), n = At(), s.c(), v(e, "class", "svelte-18tqgac"), at(
        e,
        "container",
        /*container*/
        l[7]
      );
    },
    m(r, u) {
      G(r, e, u), We(t, e, null), Sn(e, n), a[i].m(e, null), o = !0;
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
      i = _(r), i === w ? a[i].p(r, u) : (Re(), $(a[w], 1, 1, () => {
        a[w] = null;
      }), Xe(), s = a[i], s ? s.p(r, u) : (s = a[i] = f[i](r), s.c()), W(s, 1), s.m(e, null)), (!o || u[0] & /*container*/
      128) && at(
        e,
        "container",
        /*container*/
        r[7]
      );
    },
    i(r) {
      o || (W(t.$$.fragment, r), W(s), o = !0);
    },
    o(r) {
      $(t.$$.fragment, r), $(s), o = !1;
    },
    d(r) {
      r && X(e), Oe(t), a[i].d();
    }
  };
}
function Kn(l, e, t) {
  console.log("fabrie_textbox");
  let { value: n = "" } = e, { value_is_output: i = !1 } = e, { lines: s = 1 } = e, { placeholder: o = "Type here..." } = e, { label: f } = e, { info: a = void 0 } = e, { disabled: _ = !1 } = e, { show_label: r = !0 } = e, { container: u = !0 } = e, { max_lines: m } = e, { type: w = "text" } = e, { show_copy_button: q = !1 } = e, { rtl: M = !1 } = e, { autofocus: S = !1 } = e, { text_align: z = void 0 } = e, { autoscroll: F = !0 } = e, c, y = !1, N, g, A = 0, Z = !1;
  const E = Bn();
  Nn(() => {
    g = c && c.offsetHeight + c.scrollTop > c.scrollHeight - 100;
  });
  const I = () => {
    g && F && !Z && c.scrollTo(0, c.scrollHeight);
  };
  function fe() {
    E("change", n), i || E("input");
  }
  En(() => {
    S && c.focus(), g && F && I(), t(21, i = !1);
  });
  async function ue() {
    "clipboard" in navigator && (await navigator.clipboard.writeText(n), U());
  }
  function U() {
    t(15, y = !0), N && clearTimeout(N), N = setTimeout(
      () => {
        t(15, y = !1);
      },
      1e3
    );
  }
  function J(d) {
    const B = d.target, te = B.value, Q = [B.selectionStart, B.selectionEnd];
    E("select", { value: te.substring(...Q), index: Q });
  }
  async function P(d) {
    await _t(), (d.key === "Enter" && d.shiftKey && s > 1 || d.key === "Enter" && !d.shiftKey && s === 1 && m >= 1) && (d.preventDefault(), E("submit"));
  }
  function ce(d) {
    const B = d.target, te = B.scrollTop;
    te < A && (Z = !0), A = te;
    const Q = B.scrollHeight - B.clientHeight;
    te >= Q && (Z = !1);
  }
  async function ee(d) {
    if (await _t(), s === m)
      return;
    let B = m === void 0 ? !1 : m === void 0 ? 21 * 11 : 21 * (m + 1), te = 21 * (s + 1);
    const Q = d.target;
    let ye;
    B && Q.scrollHeight > B ? ye = B : Q.scrollHeight < te ? ye = te : ye = Q.scrollHeight, Q.style.height = `${ye}px`;
  }
  function b(d, B) {
    if (s !== m && (d.style.overflowY = "scroll", d.addEventListener("input", ee), !!B.trim()))
      return ee({ target: d }), {
        destroy: () => d.removeEventListener("input", ee)
      };
  }
  function Se(d) {
    ie.call(this, l, d);
  }
  function Fe(d) {
    ie.call(this, l, d);
  }
  function Pe(d) {
    ie.call(this, l, d);
  }
  function je(d) {
    ie.call(this, l, d);
  }
  function h(d) {
    ie.call(this, l, d);
  }
  function Kt(d) {
    ie.call(this, l, d);
  }
  function Xt(d) {
    ie.call(this, l, d);
  }
  function Gt(d) {
    ie.call(this, l, d);
  }
  function Ot() {
    n = this.value, t(0, n);
  }
  function Rt(d) {
    Le[d ? "unshift" : "push"](() => {
      c = d, t(14, c);
    });
  }
  function Wt() {
    n = this.value, t(0, n);
  }
  function Jt(d) {
    Le[d ? "unshift" : "push"](() => {
      c = d, t(14, c);
    });
  }
  function Qt() {
    n = this.value, t(0, n);
  }
  function xt(d) {
    Le[d ? "unshift" : "push"](() => {
      c = d, t(14, c);
    });
  }
  function $t() {
    n = this.value, t(0, n);
  }
  function el(d) {
    Le[d ? "unshift" : "push"](() => {
      c = d, t(14, c);
    });
  }
  return l.$$set = (d) => {
    "value" in d && t(0, n = d.value), "value_is_output" in d && t(21, i = d.value_is_output), "lines" in d && t(1, s = d.lines), "placeholder" in d && t(2, o = d.placeholder), "label" in d && t(3, f = d.label), "info" in d && t(4, a = d.info), "disabled" in d && t(5, _ = d.disabled), "show_label" in d && t(6, r = d.show_label), "container" in d && t(7, u = d.container), "max_lines" in d && t(8, m = d.max_lines), "type" in d && t(9, w = d.type), "show_copy_button" in d && t(10, q = d.show_copy_button), "rtl" in d && t(11, M = d.rtl), "autofocus" in d && t(12, S = d.autofocus), "text_align" in d && t(13, z = d.text_align), "autoscroll" in d && t(22, F = d.autoscroll);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    1 && n === null && t(0, n = ""), l.$$.dirty[0] & /*value, el, lines, max_lines*/
    16643 && c && s !== m && ee({ target: c }), l.$$.dirty[0] & /*value*/
    1 && fe();
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
    c,
    y,
    ue,
    J,
    P,
    ce,
    b,
    i,
    F,
    Se,
    Fe,
    Pe,
    je,
    h,
    Kt,
    Xt,
    Gt,
    Ot,
    Rt,
    Wt,
    Jt,
    Qt,
    xt,
    $t,
    el
  ];
}
class Xn extends yn {
  constructor(e) {
    super(), Ln(
      this,
      e,
      Kn,
      Yn,
      Vn,
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
function he(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
const {
  SvelteComponent: Gn,
  append: Y,
  attr: C,
  component_subscribe: ut,
  detach: On,
  element: Rn,
  init: Wn,
  insert: Jn,
  noop: ct,
  safe_not_equal: Qn,
  set_style: Te,
  svg_element: K,
  toggle_class: dt
} = window.__gradio__svelte__internal, { onMount: xn } = window.__gradio__svelte__internal;
function $n(l) {
  let e, t, n, i, s, o, f, a, _, r, u, m;
  return {
    c() {
      e = Rn("div"), t = K("svg"), n = K("g"), i = K("path"), s = K("path"), o = K("path"), f = K("path"), a = K("g"), _ = K("path"), r = K("path"), u = K("path"), m = K("path"), C(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), C(i, "fill", "#FF7C00"), C(i, "fill-opacity", "0.4"), C(i, "class", "svelte-43sxxs"), C(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), C(s, "fill", "#FF7C00"), C(s, "class", "svelte-43sxxs"), C(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), C(o, "fill", "#FF7C00"), C(o, "fill-opacity", "0.4"), C(o, "class", "svelte-43sxxs"), C(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), C(f, "fill", "#FF7C00"), C(f, "class", "svelte-43sxxs"), Te(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), C(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), C(_, "fill", "#FF7C00"), C(_, "fill-opacity", "0.4"), C(_, "class", "svelte-43sxxs"), C(r, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), C(r, "fill", "#FF7C00"), C(r, "class", "svelte-43sxxs"), C(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), C(u, "fill", "#FF7C00"), C(u, "fill-opacity", "0.4"), C(u, "class", "svelte-43sxxs"), C(m, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), C(m, "fill", "#FF7C00"), C(m, "class", "svelte-43sxxs"), Te(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), C(t, "viewBox", "-1200 -1200 3000 3000"), C(t, "fill", "none"), C(t, "xmlns", "http://www.w3.org/2000/svg"), C(t, "class", "svelte-43sxxs"), C(e, "class", "svelte-43sxxs"), dt(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(w, q) {
      Jn(w, e, q), Y(e, t), Y(t, n), Y(n, i), Y(n, s), Y(n, o), Y(n, f), Y(t, a), Y(a, _), Y(a, r), Y(a, u), Y(a, m);
    },
    p(w, [q]) {
      q & /*$top*/
      2 && Te(n, "transform", "translate(" + /*$top*/
      w[1][0] + "px, " + /*$top*/
      w[1][1] + "px)"), q & /*$bottom*/
      4 && Te(a, "transform", "translate(" + /*$bottom*/
      w[2][0] + "px, " + /*$bottom*/
      w[2][1] + "px)"), q & /*margin*/
      1 && dt(
        e,
        "margin",
        /*margin*/
        w[0]
      );
    },
    i: ct,
    o: ct,
    d(w) {
      w && On(e);
    }
  };
}
function ei(l, e, t) {
  let n, i, { margin: s = !0 } = e;
  const o = ft([0, 0]);
  ut(l, o, (m) => t(1, n = m));
  const f = ft([0, 0]);
  ut(l, f, (m) => t(2, i = m));
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
  return xn(() => (u(), () => a = !0)), l.$$set = (m) => {
    "margin" in m && t(0, s = m.margin);
  }, [s, n, i, o, f];
}
class ti extends Gn {
  constructor(e) {
    super(), Wn(this, e, ei, $n, Qn, { margin: 0 });
  }
}
const {
  SvelteComponent: li,
  append: _e,
  attr: O,
  binding_callbacks: mt,
  check_outros: It,
  create_component: ni,
  create_slot: ii,
  destroy_component: si,
  destroy_each: Ut,
  detach: p,
  element: x,
  empty: ve,
  ensure_array_like: He,
  get_all_dirty_from_scope: oi,
  get_slot_changes: fi,
  group_outros: Yt,
  init: ai,
  insert: k,
  mount_component: _i,
  noop: Ke,
  safe_not_equal: ri,
  set_data: D,
  set_style: se,
  space: R,
  text: T,
  toggle_class: j,
  transition_in: pe,
  transition_out: ke,
  update_slot_base: ui
} = window.__gradio__svelte__internal, { tick: ci } = window.__gradio__svelte__internal, { onDestroy: di } = window.__gradio__svelte__internal, mi = (l) => ({}), bt = (l) => ({});
function ht(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n[40] = t, n;
}
function gt(l, e, t) {
  const n = l.slice();
  return n[38] = e[t], n;
}
function bi(l) {
  let e, t = (
    /*i18n*/
    l[1]("common.error") + ""
  ), n, i, s;
  const o = (
    /*#slots*/
    l[29].error
  ), f = ii(
    o,
    l,
    /*$$scope*/
    l[28],
    bt
  );
  return {
    c() {
      e = x("span"), n = T(t), i = R(), f && f.c(), O(e, "class", "error svelte-1txqlrd");
    },
    m(a, _) {
      k(a, e, _), _e(e, n), k(a, i, _), f && f.m(a, _), s = !0;
    },
    p(a, _) {
      (!s || _[0] & /*i18n*/
      2) && t !== (t = /*i18n*/
      a[1]("common.error") + "") && D(n, t), f && f.p && (!s || _[0] & /*$$scope*/
      268435456) && ui(
        f,
        o,
        a,
        /*$$scope*/
        a[28],
        s ? fi(
          o,
          /*$$scope*/
          a[28],
          _,
          mi
        ) : oi(
          /*$$scope*/
          a[28]
        ),
        bt
      );
    },
    i(a) {
      s || (pe(f, a), s = !0);
    },
    o(a) {
      ke(f, a), s = !1;
    },
    d(a) {
      a && (p(e), p(i)), f && f.d(a);
    }
  };
}
function hi(l) {
  let e, t, n, i, s, o, f, a, _, r = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && wt(l)
  );
  function u(c, y) {
    if (
      /*progress*/
      c[7]
    )
      return pi;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    )
      return wi;
    if (
      /*queue_position*/
      c[2] === 0
    )
      return gi;
  }
  let m = u(l), w = m && m(l), q = (
    /*timer*/
    l[5] && vt(l)
  );
  const M = [qi, yi], S = [];
  function z(c, y) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = z(l)) && (o = S[s] = M[s](l));
  let F = !/*timer*/
  l[5] && Tt(l);
  return {
    c() {
      r && r.c(), e = R(), t = x("div"), w && w.c(), n = R(), q && q.c(), i = R(), o && o.c(), f = R(), F && F.c(), a = ve(), O(t, "class", "progress-text svelte-1txqlrd"), j(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), j(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(c, y) {
      r && r.m(c, y), k(c, e, y), k(c, t, y), w && w.m(t, null), _e(t, n), q && q.m(t, null), k(c, i, y), ~s && S[s].m(c, y), k(c, f, y), F && F.m(c, y), k(c, a, y), _ = !0;
    },
    p(c, y) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? r ? r.p(c, y) : (r = wt(c), r.c(), r.m(e.parentNode, e)) : r && (r.d(1), r = null), m === (m = u(c)) && w ? w.p(c, y) : (w && w.d(1), w = m && m(c), w && (w.c(), w.m(t, n))), /*timer*/
      c[5] ? q ? q.p(c, y) : (q = vt(c), q.c(), q.m(t, null)) : q && (q.d(1), q = null), (!_ || y[0] & /*variant*/
      256) && j(
        t,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!_ || y[0] & /*variant*/
      256) && j(
        t,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let N = s;
      s = z(c), s === N ? ~s && S[s].p(c, y) : (o && (Yt(), ke(S[N], 1, 1, () => {
        S[N] = null;
      }), It()), ~s ? (o = S[s], o ? o.p(c, y) : (o = S[s] = M[s](c), o.c()), pe(o, 1), o.m(f.parentNode, f)) : o = null), /*timer*/
      c[5] ? F && (F.d(1), F = null) : F ? F.p(c, y) : (F = Tt(c), F.c(), F.m(a.parentNode, a));
    },
    i(c) {
      _ || (pe(o), _ = !0);
    },
    o(c) {
      ke(o), _ = !1;
    },
    d(c) {
      c && (p(e), p(t), p(i), p(f), p(a)), r && r.d(c), w && w.d(), q && q.d(), ~s && S[s].d(c), F && F.d(c);
    }
  };
}
function wt(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = x("div"), O(e, "class", "eta-bar svelte-1txqlrd"), se(e, "transform", t);
    },
    m(n, i) {
      k(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && se(e, "transform", t);
    },
    d(n) {
      n && p(e);
    }
  };
}
function gi(l) {
  let e;
  return {
    c() {
      e = T("processing |");
    },
    m(t, n) {
      k(t, e, n);
    },
    p: Ke,
    d(t) {
      t && p(e);
    }
  };
}
function wi(l) {
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
      f[2] + 1 + "") && D(n, t), a[0] & /*queue_size*/
      8 && D(
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
function pi(l) {
  let e, t = He(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = kt(gt(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ve();
    },
    m(i, s) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, s);
      k(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = He(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const f = gt(i, t, o);
          n[o] ? n[o].p(f, s) : (n[o] = kt(f), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && p(e), Ut(n, i);
    }
  };
}
function pt(l) {
  let e, t = (
    /*p*/
    l[38].unit + ""
  ), n, i, s = " ", o;
  function f(r, u) {
    return (
      /*p*/
      r[38].length != null ? vi : ki
    );
  }
  let a = f(l), _ = a(l);
  return {
    c() {
      _.c(), e = R(), n = T(t), i = T(" | "), o = T(s);
    },
    m(r, u) {
      _.m(r, u), k(r, e, u), k(r, n, u), k(r, i, u), k(r, o, u);
    },
    p(r, u) {
      a === (a = f(r)) && _ ? _.p(r, u) : (_.d(1), _ = a(r), _ && (_.c(), _.m(e.parentNode, e))), u[0] & /*progress*/
      128 && t !== (t = /*p*/
      r[38].unit + "") && D(n, t);
    },
    d(r) {
      r && (p(e), p(n), p(i), p(o)), _.d(r);
    }
  };
}
function ki(l) {
  let e = he(
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
      128 && e !== (e = he(
        /*p*/
        n[38].index || 0
      ) + "") && D(t, e);
    },
    d(n) {
      n && p(t);
    }
  };
}
function vi(l) {
  let e = he(
    /*p*/
    l[38].index || 0
  ) + "", t, n, i = he(
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
      128 && e !== (e = he(
        /*p*/
        o[38].index || 0
      ) + "") && D(t, e), f[0] & /*progress*/
      128 && i !== (i = he(
        /*p*/
        o[38].length
      ) + "") && D(s, i);
    },
    d(o) {
      o && (p(t), p(n), p(s));
    }
  };
}
function kt(l) {
  let e, t = (
    /*p*/
    l[38].index != null && pt(l)
  );
  return {
    c() {
      t && t.c(), e = ve();
    },
    m(n, i) {
      t && t.m(n, i), k(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[38].index != null ? t ? t.p(n, i) : (t = pt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && p(e), t && t.d(n);
    }
  };
}
function vt(l) {
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
      1048576 && D(
        e,
        /*formatted_timer*/
        s[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && D(n, t);
    },
    d(s) {
      s && (p(e), p(n), p(i));
    }
  };
}
function yi(l) {
  let e, t;
  return e = new ti({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      ni(e.$$.fragment);
    },
    m(n, i) {
      _i(e, n, i), t = !0;
    },
    p(n, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      n[8] === "default"), e.$set(s);
    },
    i(n) {
      t || (pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ke(e.$$.fragment, n), t = !1;
    },
    d(n) {
      si(e, n);
    }
  };
}
function qi(l) {
  let e, t, n, i, s, o = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && yt(l)
  );
  return {
    c() {
      e = x("div"), t = x("div"), f && f.c(), n = R(), i = x("div"), s = x("div"), O(t, "class", "progress-level-inner svelte-1txqlrd"), O(s, "class", "progress-bar svelte-1txqlrd"), se(s, "width", o), O(i, "class", "progress-bar-wrap svelte-1txqlrd"), O(e, "class", "progress-level svelte-1txqlrd");
    },
    m(a, _) {
      k(a, e, _), _e(e, t), f && f.m(t, null), _e(e, n), _e(e, i), _e(i, s), l[30](s);
    },
    p(a, _) {
      /*progress*/
      a[7] != null ? f ? f.p(a, _) : (f = yt(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), _[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      a[15] * 100}%`) && se(s, "width", o);
    },
    i: Ke,
    o: Ke,
    d(a) {
      a && p(e), f && f.d(), l[30](null);
    }
  };
}
function yt(l) {
  let e, t = He(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Lt(ht(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = ve();
    },
    m(i, s) {
      for (let o = 0; o < n.length; o += 1)
        n[o] && n[o].m(i, s);
      k(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = He(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < t.length; o += 1) {
          const f = ht(i, t, o);
          n[o] ? n[o].p(f, s) : (n[o] = Lt(f), n[o].c(), n[o].m(e.parentNode, e));
        }
        for (; o < n.length; o += 1)
          n[o].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && p(e), Ut(n, i);
    }
  };
}
function qt(l) {
  let e, t, n, i, s = (
    /*i*/
    l[40] !== 0 && Ci()
  ), o = (
    /*p*/
    l[38].desc != null && Ct(l)
  ), f = (
    /*p*/
    l[38].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null && St()
  ), a = (
    /*progress_level*/
    l[14] != null && Ft(l)
  );
  return {
    c() {
      s && s.c(), e = R(), o && o.c(), t = R(), f && f.c(), n = R(), a && a.c(), i = ve();
    },
    m(_, r) {
      s && s.m(_, r), k(_, e, r), o && o.m(_, r), k(_, t, r), f && f.m(_, r), k(_, n, r), a && a.m(_, r), k(_, i, r);
    },
    p(_, r) {
      /*p*/
      _[38].desc != null ? o ? o.p(_, r) : (o = Ct(_), o.c(), o.m(t.parentNode, t)) : o && (o.d(1), o = null), /*p*/
      _[38].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[40]
      ] != null ? f || (f = St(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      _[14] != null ? a ? a.p(_, r) : (a = Ft(_), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(_) {
      _ && (p(e), p(t), p(n), p(i)), s && s.d(_), o && o.d(_), f && f.d(_), a && a.d(_);
    }
  };
}
function Ci(l) {
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
function Ct(l) {
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
      n[38].desc + "") && D(t, e);
    },
    d(n) {
      n && p(t);
    }
  };
}
function St(l) {
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
function Ft(l) {
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
      ] || 0)).toFixed(1) + "") && D(t, e);
    },
    d(i) {
      i && (p(t), p(n));
    }
  };
}
function Lt(l) {
  let e, t = (
    /*p*/
    (l[38].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[40]
    ] != null) && qt(l)
  );
  return {
    c() {
      t && t.c(), e = ve();
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
      ] != null ? t ? t.p(n, i) : (t = qt(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && p(e), t && t.d(n);
    }
  };
}
function Tt(l) {
  let e, t;
  return {
    c() {
      e = x("p"), t = T(
        /*loading_text*/
        l[9]
      ), O(e, "class", "loading svelte-1txqlrd");
    },
    m(n, i) {
      k(n, e, i), _e(e, t);
    },
    p(n, i) {
      i[0] & /*loading_text*/
      512 && D(
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
function Si(l) {
  let e, t, n, i, s;
  const o = [hi, bi], f = [];
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
      e = x("div"), n && n.c(), O(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-1txqlrd"), j(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), j(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), j(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), j(
        e,
        "border",
        /*border*/
        l[12]
      ), se(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), se(
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
      t = a(_), t === u ? ~t && f[t].p(_, r) : (n && (Yt(), ke(f[u], 1, 1, () => {
        f[u] = null;
      }), It()), ~t ? (n = f[t], n ? n.p(_, r) : (n = f[t] = o[t](_), n.c()), pe(n, 1), n.m(e, null)) : n = null), (!s || r[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-1txqlrd")) && O(e, "class", i), (!s || r[0] & /*variant, show_progress, status, show_progress*/
      336) && j(e, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!s || r[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && j(
        e,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!s || r[0] & /*variant, show_progress, status*/
      336) && j(
        e,
        "generating",
        /*status*/
        _[4] === "generating"
      ), (!s || r[0] & /*variant, show_progress, border*/
      4416) && j(
        e,
        "border",
        /*border*/
        _[12]
      ), r[0] & /*absolute*/
      1024 && se(
        e,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), r[0] & /*absolute*/
      1024 && se(
        e,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      s || (pe(n), s = !0);
    },
    o(_) {
      ke(n), s = !1;
    },
    d(_) {
      _ && p(e), ~t && f[t].d(), l[31](null);
    }
  };
}
let Ve = [], Ue = !1;
async function Fi(l, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (Ve.push(l), !Ue)
      Ue = !0;
    else
      return;
    await ci(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let n = 0; n < Ve.length; n++) {
        const s = Ve[n].getBoundingClientRect();
        (n === 0 || s.top + window.scrollY <= t[0]) && (t[0] = s.top + window.scrollY, t[1] = n);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Ue = !1, Ve = [];
    });
  }
}
function Li(l, e, t) {
  let n, { $$slots: i = {}, $$scope: s } = e, { i18n: o } = e, { eta: f = null } = e, { queue: a = !1 } = e, { queue_position: _ } = e, { queue_size: r } = e, { status: u } = e, { scroll_to_output: m = !1 } = e, { timer: w = !0 } = e, { show_progress: q = "full" } = e, { message: M = null } = e, { progress: S = null } = e, { variant: z = "default" } = e, { loading_text: F = "Loading..." } = e, { absolute: c = !0 } = e, { translucent: y = !1 } = e, { border: N = !1 } = e, { autoscroll: g } = e, A, Z = !1, E = 0, I = 0, fe = null, ue = 0, U = null, J, P = null, ce = !0;
  const ee = () => {
    t(25, E = performance.now()), t(26, I = 0), Z = !0, b();
  };
  function b() {
    requestAnimationFrame(() => {
      t(26, I = (performance.now() - E) / 1e3), Z && b();
    });
  }
  function Se() {
    t(26, I = 0), Z && (Z = !1);
  }
  di(() => {
    Z && Se();
  });
  let Fe = null;
  function Pe(h) {
    mt[h ? "unshift" : "push"](() => {
      P = h, t(16, P), t(7, S), t(14, U), t(15, J);
    });
  }
  function je(h) {
    mt[h ? "unshift" : "push"](() => {
      A = h, t(13, A);
    });
  }
  return l.$$set = (h) => {
    "i18n" in h && t(1, o = h.i18n), "eta" in h && t(0, f = h.eta), "queue" in h && t(21, a = h.queue), "queue_position" in h && t(2, _ = h.queue_position), "queue_size" in h && t(3, r = h.queue_size), "status" in h && t(4, u = h.status), "scroll_to_output" in h && t(22, m = h.scroll_to_output), "timer" in h && t(5, w = h.timer), "show_progress" in h && t(6, q = h.show_progress), "message" in h && t(23, M = h.message), "progress" in h && t(7, S = h.progress), "variant" in h && t(8, z = h.variant), "loading_text" in h && t(9, F = h.loading_text), "absolute" in h && t(10, c = h.absolute), "translucent" in h && t(11, y = h.translucent), "border" in h && t(12, N = h.border), "autoscroll" in h && t(24, g = h.autoscroll), "$$scope" in h && t(28, s = h.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (f === null ? t(0, f = fe) : a && t(0, f = (performance.now() - E) / 1e3 + f), f != null && (t(19, Fe = f.toFixed(1)), t(27, fe = f))), l.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && t(17, ue = f === null || f <= 0 || !I ? null : Math.min(I / f, 1)), l.$$.dirty[0] & /*progress*/
    128 && S != null && t(18, ce = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (S != null ? t(14, U = S.map((h) => {
      if (h.index != null && h.length != null)
        return h.index / h.length;
      if (h.progress != null)
        return h.progress;
    })) : t(14, U = null), U ? (t(15, J = U[U.length - 1]), P && (J === 0 ? t(16, P.style.transition = "0", P) : t(16, P.style.transition = "150ms", P))) : t(15, J = void 0)), l.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? ee() : Se()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && A && m && (u === "pending" || u === "complete") && Fi(A, g), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = I.toFixed(1));
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
    c,
    y,
    N,
    A,
    U,
    J,
    P,
    ue,
    ce,
    Fe,
    n,
    a,
    m,
    M,
    g,
    E,
    I,
    fe,
    s,
    i,
    Pe,
    je
  ];
}
class Ti extends li {
  constructor(e) {
    super(), ai(
      this,
      e,
      Li,
      Si,
      ri,
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
  SvelteComponent: Vi,
  add_iframe_resize_listener: zi,
  add_render_callback: Mi,
  append: Ni,
  attr: Ei,
  binding_callbacks: Bi,
  detach: Hi,
  element: Zi,
  init: Pi,
  insert: ji,
  noop: Vt,
  safe_not_equal: Di,
  set_data: Ai,
  text: Ii,
  toggle_class: be
} = window.__gradio__svelte__internal, { onMount: Ui } = window.__gradio__svelte__internal;
function Yi(l) {
  let e, t, n;
  return {
    c() {
      e = Zi("div"), t = Ii(
        /*value*/
        l[0]
      ), Ei(e, "class", "svelte-84cxb8"), Mi(() => (
        /*div_elementresize_handler*/
        l[5].call(e)
      )), be(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), be(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), be(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    m(i, s) {
      ji(i, e, s), Ni(e, t), n = zi(
        e,
        /*div_elementresize_handler*/
        l[5].bind(e)
      ), l[6](e);
    },
    p(i, [s]) {
      s & /*value*/
      1 && Ai(
        t,
        /*value*/
        i[0]
      ), s & /*type*/
      2 && be(
        e,
        "table",
        /*type*/
        i[1] === "table"
      ), s & /*type*/
      2 && be(
        e,
        "gallery",
        /*type*/
        i[1] === "gallery"
      ), s & /*selected*/
      4 && be(
        e,
        "selected",
        /*selected*/
        i[2]
      );
    },
    i: Vt,
    o: Vt,
    d(i) {
      i && Hi(e), n(), l[6](null);
    }
  };
}
function Ki(l, e, t) {
  let { value: n } = e, { type: i } = e, { selected: s = !1 } = e, o, f;
  function a(u, m) {
    !u || !m || (f.style.setProperty("--local-text-width", `${m < 150 ? m : 200}px`), t(4, f.style.whiteSpace = "unset", f));
  }
  Ui(() => {
    a(f, o);
  });
  function _() {
    o = this.clientWidth, t(3, o);
  }
  function r(u) {
    Bi[u ? "unshift" : "push"](() => {
      f = u, t(4, f);
    });
  }
  return l.$$set = (u) => {
    "value" in u && t(0, n = u.value), "type" in u && t(1, i = u.type), "selected" in u && t(2, s = u.selected);
  }, [n, i, s, o, f, _, r];
}
class ss extends Vi {
  constructor(e) {
    super(), Pi(this, e, Ki, Yi, Di, { value: 0, type: 1, selected: 2 });
  }
}
const {
  SvelteComponent: Xi,
  add_flush_callback: zt,
  assign: Gi,
  bind: Mt,
  binding_callbacks: Nt,
  check_outros: Oi,
  create_component: Je,
  destroy_component: Qe,
  detach: Ri,
  flush: L,
  get_spread_object: Wi,
  get_spread_update: Ji,
  group_outros: Qi,
  init: xi,
  insert: $i,
  mount_component: xe,
  safe_not_equal: es,
  space: ts,
  transition_in: ge,
  transition_out: Ce
} = window.__gradio__svelte__internal;
function Et(l) {
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
    i = Gi(i, n[s]);
  return e = new Ti({ props: i }), {
    c() {
      Je(e.$$.fragment);
    },
    m(s, o) {
      xe(e, s, o), t = !0;
    },
    p(s, o) {
      const f = o[0] & /*gradio, loading_status*/
      131076 ? Ji(n, [
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
        131072 && Wi(
          /*loading_status*/
          s[17]
        )
      ]) : {};
      e.$set(f);
    },
    i(s) {
      t || (ge(e.$$.fragment, s), t = !0);
    },
    o(s) {
      Ce(e.$$.fragment, s), t = !1;
    },
    d(s) {
      Qe(e, s);
    }
  };
}
function ls(l) {
  let e, t, n, i, s, o = (
    /*loading_status*/
    l[17] && Et(l)
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
    l[1]), t = new Xn({ props: _ }), Nt.push(() => Mt(t, "value", f)), Nt.push(() => Mt(t, "value_is_output", a)), t.$on(
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
        o && o.c(), e = ts(), Je(t.$$.fragment);
      },
      m(r, u) {
        o && o.m(r, u), $i(r, e, u), xe(t, r, u), s = !0;
      },
      p(r, u) {
        /*loading_status*/
        r[17] ? o ? (o.p(r, u), u[0] & /*loading_status*/
        131072 && ge(o, 1)) : (o = Et(r), o.c(), ge(o, 1), o.m(e.parentNode, e)) : o && (Qi(), Ce(o, 1, 1, () => {
          o = null;
        }), Oi());
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
        r[0], zt(() => n = !1)), !i && u[0] & /*value_is_output*/
        2 && (i = !0, m.value_is_output = /*value_is_output*/
        r[1], zt(() => i = !1)), t.$set(m);
      },
      i(r) {
        s || (ge(o), ge(t.$$.fragment, r), s = !0);
      },
      o(r) {
        Ce(o), Ce(t.$$.fragment, r), s = !1;
      },
      d(r) {
        r && Ri(e), o && o.d(r), Qe(t, r);
      }
    }
  );
}
function ns(l) {
  let e, t;
  return e = new hl({
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
      $$slots: { default: [ls] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Je(e.$$.fragment);
    },
    m(n, i) {
      xe(e, n, i), t = !0;
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
      t || (ge(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ce(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Qe(e, n);
    }
  };
}
function is(l, e, t) {
  let { gradio: n } = e, { label: i = "Textbox" } = e, { info: s = void 0 } = e, { elem_id: o = "" } = e, { elem_classes: f = [] } = e, { visible: a = !0 } = e, { value: _ = "" } = e, { lines: r } = e, { placeholder: u = "" } = e, { show_label: m } = e, { max_lines: w } = e, { type: q = "text" } = e, { container: M = !0 } = e, { scale: S = null } = e, { min_width: z = void 0 } = e, { show_copy_button: F = !1 } = e, { loading_status: c = void 0 } = e, { value_is_output: y = !1 } = e, { rtl: N = !1 } = e, { text_align: g = void 0 } = e, { autofocus: A = !1 } = e, { autoscroll: Z = !0 } = e, { interactive: E } = e;
  function I(b) {
    _ = b, t(0, _);
  }
  function fe(b) {
    y = b, t(1, y);
  }
  const ue = () => n.dispatch("change", _), U = () => n.dispatch("input"), J = () => n.dispatch("submit"), P = () => n.dispatch("blur"), ce = (b) => n.dispatch("select", b.detail), ee = () => n.dispatch("focus");
  return l.$$set = (b) => {
    "gradio" in b && t(2, n = b.gradio), "label" in b && t(3, i = b.label), "info" in b && t(4, s = b.info), "elem_id" in b && t(5, o = b.elem_id), "elem_classes" in b && t(6, f = b.elem_classes), "visible" in b && t(7, a = b.visible), "value" in b && t(0, _ = b.value), "lines" in b && t(8, r = b.lines), "placeholder" in b && t(9, u = b.placeholder), "show_label" in b && t(10, m = b.show_label), "max_lines" in b && t(11, w = b.max_lines), "type" in b && t(12, q = b.type), "container" in b && t(13, M = b.container), "scale" in b && t(14, S = b.scale), "min_width" in b && t(15, z = b.min_width), "show_copy_button" in b && t(16, F = b.show_copy_button), "loading_status" in b && t(17, c = b.loading_status), "value_is_output" in b && t(1, y = b.value_is_output), "rtl" in b && t(18, N = b.rtl), "text_align" in b && t(19, g = b.text_align), "autofocus" in b && t(20, A = b.autofocus), "autoscroll" in b && t(21, Z = b.autoscroll), "interactive" in b && t(22, E = b.interactive);
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
    c,
    N,
    g,
    A,
    Z,
    E,
    I,
    fe,
    ue,
    U,
    J,
    P,
    ce,
    ee
  ];
}
class os extends Xi {
  constructor(e) {
    super(), xi(
      this,
      e,
      is,
      ns,
      es,
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
  ss as BaseExample,
  Xn as BaseTextbox,
  os as default
};
