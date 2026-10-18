function hexdiff_DBoqm(varargin)
% hexdiff_DBoqm (0)b Evergreen / No Date - JP DEV READY
% MATLAB/Octave version of hexdiff_DBoqm.com 263b
% Usage: main or main('old.bin','new.bin')
% In repo: demo-repository/santberk/main.m

fprintf('hexdiff_DBoqm (0)b Evergreen - No Date\n');
if nargin < 2
  f1 = fullfile(getenv('HOME'),'oeneye','NASMusbOQM_OMQ.com');
  % old version simulated as first 276 bytes vs new 850
  f1_old = f1;
  f2 = f1;
  fprintf('FILE1: NASMusbOQM_OMQ.com old (276) $\n');
  fprintf('FILE2: NASMusbOQM_OMQ.com new (850) $\n');
else
  f1 = varargin{1}; f2 = varargin{2};
end

% Read
try
  b1 = fileread_bin(f1);
  b2 = fileread_bin(f2);
catch
  % demo data if files missing on GitHub runner
  b1 = uint8(0:63);
  b2 = uint8([0:31, 255, 33:63]);
end

% BUS0 canary: JC (0)b - carry if diff
n = min(numel(b1), numel(b2));
diffs = find(b1(1:n) ~= b2(1:n));

if isempty(diffs)
  fprintf('OQM OMQ: BUS0 OK - canary loop closed - no diff %d bytes\n', n);
else
  for k=diffs(:)'
    fprintf('DIFF at %04X : %02X -> %02X  (0)b FAIL JC\n', k-1, b1(k), b2(k));
    % (0)b binary mode canary
    if bitget(b1(k),1) ~= bitget(b2(k),1)
      fprintf('  -> BUS0 bit0 canary flipped!\n');
    end
  end
  fprintf('OQM FAIL JC (0)b - %d diffs\n', numel(diffs));
end

% hexdump 64 bytes like .com
fprintf('\n-- hexdump first 64 --\n');
dump_hex(b1(1:min(64,end)));
end

function b = fileread_bin(p)
  fid=fopen(p,'rb'); b=fread(fid,'*uint8')'; fclose(fid);
end
function dump_hex(b)
  for i=1:numel(b)
    fprintf('%02X ', b(i));
    if mod(i,16)==0, fprintf('\n'); end
  end
  fprintf('\n');
end
