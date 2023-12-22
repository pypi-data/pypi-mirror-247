Módulo para arreglar el error de haber usado tarifas de venta a depósito cuando deberían haber sido a venta directa.

Para ello, en las ventas que tengan una tarifa con ruta de venta directa y además tengan transferencias desde depósito adociadas y siempre y cuando la transferencia a depósito esté validada (estado = hecho), se validarán las tranferencias desde depósito por completo mediante este script.
