with open("oeneye_monograph.tex", "r") as f:
    content = f.read()

insertion = r"""
\section{Terminal Typography and Bitmap Font Architecture}
The runtime core utilizes the fixed-size binary font asset \texttt{OMQ.FNT} for low-level framebuffer and text-mode console rendering.

\begin{itemize}
    \item \textbf{Asset Specification}: \texttt{OMQ.FNT} (4096-byte raw binary bitmap font).
    \item \textbf{Glyph Matrix Dimensions}: Standard 8x16 or equivalent fixed-pitch grid mapping across the 256-character extended ASCII set ($16 \text{ bytes/glyph} \times 256 = 4096 \text{ bytes}$).
    \item \textbf{Storage Subsystem}: Indexed within the FAT12 immutable core floppy architecture under the \texttt{FONT/} hierarchy, ensuring zero-latency retrieval during early kernel initialization prior to userland handoff.
\end{itemize}
"""

if "Terminal Typography" not in content:
    content = content.replace("\\end{document}", insertion + "\n\\end{document}")
    with open("oeneye_monograph.tex", "w") as f:
        f.write(content)
    print("Monograph successfully patched!")
else:
    print("Monograph already contains the typography section.")
