class HoldInfo:
    _trade_date = None
    _underly_sec_syb = ""
    _num_shares_hold_long = 0
    _num_shares_hold_short = 0
    _total_issued_shares = 0
    _pct_long = 0
    _pct_short = 0

    def __str__(self):
        return self._trade_date.strftime("%Y-%m-%d")\
        +","+self._underly_sec_syb\
        +","+str(self._num_shares_hold_long)\
        +","+str(self._num_shares_hold_short)\
        +","+str(self._total_issued_shares)\
        +","+str(self._pct_long)\
        +","+str(self._pct_short)
