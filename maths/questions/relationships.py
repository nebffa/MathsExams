import inspect
import os
import pickle
import random
import copy
import re


class DummyPart:
    """A dummy question part for when a question should be structured like so:
        1. (no question text)
            a. some question
            b. some other related question
    """

    def __init__(self):
        self.num_lines, self.num_marks = 0, 0

    def sanity_check(self):
        pass


class QuestionPart:
    """Base class for all question parts.
    """

    is_root = False
    parents = []

    @classmethod
    def storage_paths(cls):
        """Return the paths that are involved in storing this class' questions.
        """
        class_path = inspect.getfile(cls)
        questions_folder, module_name = os.path.split(class_path)

        indices_folder = os.path.join(questions_folder, 'storage', 'indices')
        indices_name = '{module_name}_indices'.format(module_name=module_name)
        indices_path = os.path.join(indices_folder, indices_name)

        data_folder = os.path.join(questions_folder, 'storage', 'data')
        data_name = '{module_name}_{class_name}'.format(module_name=module_name, class_name=cls.__name__)
        data_path = os.path.join(data_folder, data_name)

        return indices_path, data_path

    @classmethod
    def store_question(cls):
        """Store all possible question numbers that have student-friendly values.
        """
        indices_path, data_path = cls.storage_paths()

        byte_indices = [0]
        with open(data_path, 'wb') as f:
            for question in cls.enumerate_questions():
                pickle.dump(question, f)
                byte_indices.append(f.tell())

        if os.path.exists(indices_path):
            with open(indices_path, 'rb') as f:
                cur_indices = pickle.load(f)
        else:
            cur_indices = {}

        cur_indices[cls.__name__] = byte_indices
        with open(indices_path, 'wb') as f:
            pickle.dump(cur_indices, f)

    @classmethod
    def scan_random_question(cls):
        """Return a random set of valid coefficients for this question.
        """
        indices_path, data_path = cls.storage_paths()

        with open(indices_path, 'rb') as f:
            all_indices = pickle.load(f)
            byte_indices = all_indices[cls.__name__]

        with open(data_path, 'rb') as f:
            question_number = random.randint(0, len(byte_indices) - 1)
            first_byte = byte_indices[question_number]
            last_byte = byte_indices[question_number + 1]

            f.seek(first_byte)
            pickled_question = f.read(last_byte - first_byte)

        return pickle.loads(pickled_question)

    def combined_question_dict(self):
        """Return the combined dictionary of a question's parameters and information.
        """

        combined = copy.deepcopy(self._qp)
        if hasattr(self, '_qi'):
            combined.update(self._qi)

        return combined


def root(cls):
    """A class decorator to specify a question root.
    """

    cls.is_root = True
    return cls


def is_child_of(*parents):
    """A class decorator to specify a part's parent.
    """

    def decorator(cls):
        cls.parents = parents
        return cls
    return decorator


class PartTree:
    def __init__(self, cls):
        self.cls = cls
        self.children = []  # PartTrees of all the subparts

    def _find_parent(self, cls):
        """A helper function for "add_subpart".

        Given the existing question tree, find out where to insert a new part.
        """

        if self.cls in cls.parents:  # the current node is the parent
            return self
        else:  # check if any of the current node's children is the parent
            for i in self.children:
                if i._find_parent(cls):
                    return i._find_parent(cls)

        raise RuntimeError('The class: {0} could not be located in the tree'.format(cls.__name__))

    def add_subpart(self, cls):
        """Add a new class to the tree.
        """

        child = PartTree(cls)
        parent = self._find_parent(cls)
        parent.children.append(child)

    def _instantiate_tree(self, depth=0, parent=None):
        """Traverse the tree and instantiates an object of each class,
        creating a question for the student to do.
        """

        if depth == 0:  # there's no parent part
            self.object = self.cls()
        elif isinstance(parent, DummyPart):  # there is a dummy for the parent part - there's no information to inherit
            self.object = self.cls()
        else:
            self.object = self.cls(part=parent)

        for child in self.children:
            child._instantiate_tree(depth + 1, self.object)

    def _question_traversal_to_latex(self, depth=0):  # uses the enumitem package which gives us some hbox errors
        """Traverse the tree, returning the latex for each instantiated object.
        """

        total_string = r'\item' + '\n'

        if depth == 0:
            total_string += '\n'

        if not hasattr(self.object, 'question_statement'):
            total_string += '$ $'
        else:
            total_string += self.object.question_statement() + '\n'

        if self.object.num_lines != 0:
            total_string += r'\fillwithlines{{{0}in}}'.format(self.object.num_lines / 4) + '\n'

        if self.children:
            total_string += r'\begin{parts}' + '\n' + '\n'.join(
                i._question_traversal_to_latex(depth + 1) for i in self.children) + r'\end{parts}' + '\n'

        return total_string + '\n'

    def _solution_traversal_to_latex(self, depth=0):  # uses the enumitem package which gives us some hbox errors
        """Traverse the tree, returning the latex for each instantiated object.
        """

        total_string = r'\item' + '\n'

        if depth == 0:
            total_string += '\n'

        if not hasattr(self.object, 'solution_statement'):
            total_string += '$ $'
        else:
            total_string += self.object.solution_statement() + '\n'

        if self.children:
            total_string += r'\begin{parts}' + '\n' + '\n'.join(
                i._solution_traversal_to_latex(depth + 1) for i in self.children) + r'\end{parts}' + '\n'

        return total_string + '\n'

    def write_question(self, f):
        self._instantiate_tree()
        f.write(self._question_traversal_to_latex())

    def write_solution(self, f):
        f.write(self._solution_traversal_to_latex())

    def show_question(self):
        """Return a question's latex (assuming the question tree has already been populated).
        """
        self._instantiate_tree()
        return self._question_traversal_to_latex()

    def question_statement(self):
        """Return the LaTeX representing the question.
        """

        self._instantiate_tree()
        return self._question_traversal_to_latex()

    def solution_statement(self):
        """Return the LaTeX representing the solution.
        """

        return self._solution_traversal_to_latex()


def exists_dummy_parent(parts):
    """State whether there is a dummy parent for any part in a list of parts.
    """

    for part in parts:
        if DummyPart in part.parents:
            return True

    return False


def ordered_parts(module, parts):
    """Return the parts in the order they appear within the module.

    inspect.getmembers(module, inspect.isclass) will give us all the classes in a file, but in alphabetical order.

    We want the classes in the order they are defined in the module, since a part may logically come before another
    in a question, and we store that information by having it defined first.
    """

    with open(module.__file__, 'r') as f:
        module_text = f.read()

    part_locations_in_file = {}
    search_for = r'class {class_name}\('
    for part in parts:
        if part == DummyPart:  # we place dummy parts at the front since they will always be parents
            part_locations_in_file[part] = 0
            continue

        search = search_for.format(class_name=part.__name__)

        match = re.search(search, module_text)

        part_locations_in_file[part] = match.start()

    return sorted(part_locations_in_file, key=part_locations_in_file.get)


def parse_structure(module):
    """Parse the question structure based on the relationships of classes in a module.

    Will be evolved over time!!!
    """

    if hasattr(module, 'question_not_complete'):
        return None

    parts = []
    for _, member in inspect.getmembers(module, inspect.isclass):
        if issubclass(member, QuestionPart):  # get all the question parts
            parts.append(member)

    roots = [i for i in parts if i.is_root]
    if exists_dummy_parent(parts):
        roots.append(DummyPart)
        parts.append(DummyPart)

    if len(roots) == 0:
        raise RuntimeError('There must be at least 1 root or DummyPart parent in {0}'.format(module.__name__))

    def invalid_part(part):
        """Returns false for any class that neither is the question root nor has a parent.
        """

        if part == DummyPart:
            return False
        if not part.is_root and part.parents is None:
            return True
        else:
            return False

    for part in parts:
        if invalid_part(part):
            raise ValueError('The part: {0} is neither the root part nor a subpart.'.format(part.__name__))

    def build_from_root(root, parts):
        """Given a root, build a question tree out of the part heirarchy.
        """

        parts = copy.deepcopy(parts)

        tree = PartTree(root)
        parts.remove(root)

        # since we will iterate over the reversed list, we want to reverse it here so we are still
        # technically checking each part in order
        parts = list(reversed(parts))
        while parts:
            # we iterate over the reversed list so we can remove as we go, otherwise we run into unintuitive errors
            # like skipping items in the iteration
            for part in reversed(parts):
                try:
                    tree.add_subpart(part)
                except RuntimeError as e:
                    # the part could not be located in the tree
                    # we could do this a more efficient way, but we are dealing with O(1) parts so raising a couple of
                    # exceptions here won't change much
                    pass

                parts.remove(part)

        return tree

    parts = ordered_parts(module, parts)
    trees = [build_from_root(root, parts) for root in roots]

    return trees
